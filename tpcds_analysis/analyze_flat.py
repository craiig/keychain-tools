#!/usr/bin/env python

import argparse
import json
import sqlparse
import sys
from pprint import pprint
import pandas as pd
import re

parser = argparse.ArgumentParser(description='analyze flattened plans')
parser.add_argument('--filename', '-f', help='filename of plans')
parser.add_argument('--test', '-t', help='test statement to parse')
parser.add_argument('--filter', help='print all original statements that match the given string, used in conjunction with --filename')
parser.add_argument('--filter_re', help='print all original statements that match the given regex, used in conjunction with --filename')
parser.add_argument('--print_sorted', '-s', help='sort by expression before outputting', action='store_true')
args = parser.parse_args()

# The overall methodology here is to group statements together that DO NOT have
# potential variations that we need to capture.
#
# things we folded into higher level groups:
#   functions of single column
#   aggregates of single column
#   identifier names
#   coalesce replaced with it's first argument
#   binary operations, disregarding operator

###
identifier_numbering = 0;
id_map = {}

def parser_preprocess(sql):
    # needed because sql parse does not recognize bpchar as a built-in
    sql = re.sub("::bpchar", "::text", sql) # synonynms for the same type

    # SUBPLAN references:
    # we treat subplan references as basically columns because they are the
    # results of prior computations run over the data, or computations running
    # concurrently (once per row), in which case they are just treated as
    # columns on the current data set

    # 1. a subplan quirk from Postgres is that there may be optional plan
    # alternatives that are selected at runtime, so we fold them up here
    # http://grokbase.com/t/postgresql/pgsql-general/12bwsdmsg7/alternatives
    sql = re.sub("\(alternatives: SubPlan (\d+) or hashed SubPlan \d\)", "subplan.ref\\1", sql)

    #2. what is the difference between SubPlan \d and $2?
    # SubPlan is a plan that has dependencies on other parts of the query
    # InitPlan ($\d)+ references are plans that have no dependencies and can be executed once
    #  InitPlans are as good as constants assuming no updates to the underlying data happens
    #  for our purposes we group them together as one
    sql = re.sub("SubPlan (\d+)", "subplan.ref\\1", sql)
    sql = re.sub("\$(\d+)", "subplan.ref\\1", sql)

    # 3. another subplan reference fix to some subquery scans that
    # have interesting alias names, when they just seem to be normal subqueries
    sql = re.sub("\"\*SELECT\* \d+\".", "alias.", sql)

    #simplify numeric casts
    sql = re.sub("::numeric\(\d+,\d+\)", "::numeric", sql) 

    if args.test:
        print "sql post process: {}".format(sql)

    return sql

def parse(sql):
    p = sqlparse.parse(parser_preprocess(sql))[0]
    if args.test:
        print "parse: {}".format(p)
    return p

def erase_identifier_names(node, debug=False):
    global identifier_numbering, id_map
    id_map = {}
    identifier_numbering = 0;
    node = remove_outer_paranthesis(node)
    return erase_identifier_names_recur(node, debug=debug)

def remove_outer_paranthesis(node):
    #remove any outer paranthesis so we can keep it similar
    if type(node) == sqlparse.sql.Statement and len(node.tokens) == 1  and type(node.tokens[0]) == sqlparse.sql.Parenthesis:
        parans = node.tokens[0]
        while len(parans.tokens) == 3 and type(parans.tokens[1]) == sqlparse.sql.Parenthesis:
            #unroll any further nesting too
            if args.test:
                print "unroll another parans, tokens: {}".format(parans.tokens)
            parans = parans.tokens[1]

        #node.tokens = [parans.tokens[1]]
        # remove the first and last token nodes
        # test case: "((date_dim.d_date >= '1999-02-01') and (date_dim.d_date <= '1999-04-02 00:00:00'))"
        node.tokens = parans.tokens[1:-1]
        if args.test:
            print "remove outer paranthesis: {} tokens: {} parans tokens: {}".format(node, node.tokens, parans.tokens)

    if args.test:
        print "post remove outer paranthesis: {}".format(node)

    return node
    pass

def erase_identifier_names_recur(node, in_function=False, debug=False):
    # walk each parse node and modify any identifier name into basic name
    global identifier_numbering, id_map

    #set in function now, because we may unset it later when we do a coalesce replacement
    next_in_function = type(node)==sqlparse.sql.Function

    #only replace identifiers when we are not in a function and it matches the standard column name regex
    if debug:
        print "---> node: {} type: {} tokenlist: {} in_function: {}".format(
                node, type(node), isinstance(node, sqlparse.sql.TokenList), in_function)
        if hasattr(node,'tokens'):
            print "\ttokens: {}".format(node.tokens)
    if type(node) == sqlparse.sql.Identifier and not in_function and re.match("^[0-9A-z_\.]*$", node.value):
        if debug:
            print "identifier replacement"
        if re.match('^subplan_reference$', node.value):
            # skip
            name = node.value
        elif node.value not in id_map:
            #TODO we are erasing too much, what about constants????
            # maybe this is ok??
            # only replace standard column names
            name = 'identifier{}'.format(identifier_numbering)
            identifier_numbering = identifier_numbering + 1
            id_map[node.value] = name
        else:
            name = id_map[node.value]
        if debug:
            print 'old: {} new: {}'.format(node.value, name)
        node.tokens = [sqlparse.sql.Token(sqlparse.tokens.Name, name)]
    elif type(node) == sqlparse.sql.Identifier and in_function and re.match("^[0-9A-z_\.]*$", node.value):
        #replace function names
        if debug:
            print "agg replacement"
        func_renames = {
                'avg': 'agg'
                ,'sum': 'agg'
                ,'max': 'agg'
                ,'min': 'agg'
                ,'stddev_samp': 'agg'
                ,'round': 'func'
        }
        if node.value in func_renames:
            node.tokens = [sqlparse.sql.Token(sqlparse.tokens.Name, func_renames[node.value])]
    elif type(node)==sqlparse.sql.Function and node.tokens[0].value == 'COALESCE':
        #transform coalesce into just the identifier reference (first argument)
        # this is OK for our analysis because coalesce is written in a very specific way
        cand = node.tokens[1].tokens[1]
        if(type(cand) == sqlparse.sql.IdentifierList):
            #sometimes an expression list can be parsed as an identifier list, sometimes not
            # tests cases:
            #   "COALESCE(identifier0, '0'::numeric)"
            #   "sum(COALESCE((store_sales.ss_sales_price * (store_sales.ss_quantity)::numeric), '0'::numeric))"
            cand = cand.tokens[0]
        if debug:
            print "coalesce replacement candidate: {} type: {} tokens: {}".format( cand, type(cand), cand.tokens)
        if(cand.tokens[0].value == '(' and cand.tokens[-1].value == ')'):
            if debug:
                print "trimming parenthesis from coalesce in: {} out: {}".format(cand.tokens, cand.tokens[1:-1])
            cand.tokens = cand.tokens[1:-1]
        node.tokens = [cand]
        #TODO coalesce needs to trip column identifier stuff too
        #since we removed coalesce we can mark ourseles as not being in a function anymore
        next_in_function = False
        pass
    elif type(node) == sqlparse.sql.Token and (node.ttype == sqlparse.tokens.Number.Integer or node.ttype == sqlparse.tokens.Number.Float):
        #detect numeric constants
        if debug:
            print 'number: {}'.format(node)
        node.value = 'numeric_constant'
    elif type(node) == sqlparse.sql.Parenthesis:
        #fold parenthesis
        while (len(node.tokens) == 3 and 
            type(node.tokens[0]) == sqlparse.sql.Token and node.tokens[0].value == '('
            and type(node.tokens[1]) == sqlparse.sql.Parenthesis
            and type(node.tokens[2]) == sqlparse.sql.Token and node.tokens[2].value == ')'
        ):
            #unroll any further nesting too
            candidate = node.tokens[1]
            node.tokens = node.tokens[1].tokens
            #print "token[0]: {} val: {} token[1]: {} token[2]: {}".format(type(node.tokens[0]), node.tokens[0].value,  type(node.tokens[1]), type(node.tokens[2]))
            if args.test:
                print "remove nested parenthesis, candidate: {} candidate.tokens: {} node.tokens: {}".format(candidate, candidate.tokens, node.tokens)

    #recurse 
    if isinstance(node, sqlparse.sql.TokenList):
        for n in node:
            #to avoid re-writing parts of identifiers, including any casts, we won't descend into identifiers
            # this is actually preventing a re-write of an expression
            #if type(node) != sqlparse.sql.Identifier:
            erase_identifier_names_recur(n, in_function=next_in_function, debug=debug)
    if debug:
        print "<---"

    # since sqlparse stores a string value for each node
    # since we've changed the name we need to rebuild it back up
    oldval = node.value
    return node

def transform_statement(ty, stmnt):
    o = stmnt
    o = str(erase_identifier_names(parse(o)))

    r = {
        #"col" : "[0-9A-z_\.]+"
        "col" : "identifier[0-9]+"
        , "op": "(<|>|==|<=|>=|=|/|-|\*|<>|\+)"
        , "non_commute_op": "(\|\|)"
        , "text_constant": "'[^']+?'::text"
        , "date_constant": "'[^']+?'::date"
        #, "function": "[A-z]+\({col}.*?\)"
    }
    # one level of substitution lets us reference other patterns more easily
    for k in r.iterkeys():
        r[k] = r[k].format(**r)

    #o = re.sub("^'.*'::text$", "'.*'::text constant", o) 
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common
    o = re.sub("'[^']+?'::numeric".format(**r), "numeric_constant", o) 
    o = re.sub("'[^']+?'::integer".format(**r), "numeric_constant", o) 
    o = re.sub("NULL::numeric".format(**r), "numeric_constant", o) 
    o = re.sub("NULL::integer".format(**r), "numeric_constant", o) 
    o = re.sub("NULL::bigint".format(**r), "numeric_constant", o) 
    o = re.sub("'[^']+?'::timestamp without time zone", "time_constant", o)
    o = re.sub("{date_constant}".format(**r), "time_constant", o) 

    #fix numeric casts on identifiers and expressions since we don't really care
    #note some of this is in the regex preprocessor too
    o = re.sub("\(({col})\)::numeric".format(**r), "\\1", o)
    #o = re.sub("\(({col})\)text".format(**r), "\\1", o)

    #TODO stop replacing here to perform a summary of:
    # # of cols, # of identifiers, # of operators used for each query

    #high level ops
    o = re.sub("{col} ({op}) {col}".format(**r), "col op col", o)
    #o = re.sub("{col} ({op}) \({col}\)::numeric".format(**r), "col op col", o) # are these two needed?
    #o = re.sub("\({col}\)::numeric ({op}) {col}".format(**r), "col op col", o)
    o = re.sub("{col} ({op}) (numeric|text|time)_constant".format(**r), "col op constant", o)

    #some control flow patterns
    # i think a few conditional aggregations would be good to add to a test
    o = re.sub("^agg\(CASE WHEN \(.*\) THEN numeric_constant ELSE numeric_constant END\)$", "conditional aggregate", o)
    o = re.sub("^agg\(CASE WHEN \(.*\) THEN {col} ELSE numeric_constant END\)$".format(**r), "conditional aggregate", o)
    o = re.sub("agg\(CASE WHEN \(.*\) THEN .*? ELSE .*? END\)".format(**r), "conditional aggregate", o) #catch all to isolate this category entirely

    o = re.sub("^\(([^\(\)]*?)\)$", "\\1", o) #eliminate outer parenthesis as long as there are no inner paranthesis
    #o = re.sub("^sum\([0-9A-z_\.]*\)$", "sum(column)", o) #explicitly match sum
    #o = re.sub("^avg\([0-9A-z_\.]*\)$", "avg(column)", o) 
    #o = re.sub("^max\([0-9A-z_\.]*\)$", "max(column)", o) 
    #o = re.sub("^substr\([0-9A-z_\.]*\)$", "substr(column)", o) 

    #o = re.sub("^round\(\([0-9A-z_\.]*? / [0-9A-z\.]*?\), \d+\)$", "rounded_division", o)

    #o = re.sub("^{col} ({op}) {col}$".format(**r), "col1 \\1 col2", o)
    #o = re.sub("{col} ({op}) {col}".format(**r), "col1 \\1 col2", o)
    #o = re.sub("^{col} ({non_commute_op}) {col}$".format(**r), "col1 \\1 col2", o)

    #o = re.sub("{function}".format(**r), "col1 \\1 col2", o)
    #o = re.sub("{col} ({op}) {function}".format(**r), "col1 \\1 col2", o)
    return o

#want to satisfy a few queries:
# total occurences of an expression
# number of unique queries expression appears in
#
queries = [] #faster to load them all at once
def analyze_outputs(p):
    global queries

    def process_statement(query, ty, in_stmnt):
        global queries
        # TODO ignore some nodes to avoid 'over counting'
        # because basic col outputs are very high, (or we just don't report it in that way)
        #transform outputs
        # the way we'll avoid this is giving occurences relative to different queries
        # instead of relative to some 'total number of expressions'
        try: 
            out_stmnt = transform_statement(ty,in_stmnt)
        except Exception as inst:
            print "exception parsing statement: {}".format(in_stmnt)
            raise

        if args.filter and args.filter == out_stmnt:
            print in_stmnt
        if args.filter_re and re.match(args.filter_re, out_stmnt):
            print in_stmnt
 
        obj = {
            'query': query,
            'type': ty,
            'expression': out_stmnt
        }
        queries.append(obj)

    #what are the column transformations?
    if "Output" in p:
        for o in p['Output']:
            process_statement(p['filename'], 'output',o)
            pass

    if "Filter" in p:
        #print p['Filter']
        process_statement(p['filename'], 'filter',p['Filter'])
        pass

    for k in p.get("Group Key", []):
        process_statement(p['filename'], 'group', k)
        pass

    def flatten_group_sets(gsets):
        for gs in gsets:
            for gks in gs['Group Keys']:
                for k in gks:
                    yield k

    if("Grouping Sets" in p):
        groups = [item for item in flatten_group_sets(p['Grouping Sets'])]
        for g in groups:
            process_statement(p['filename'], 'group', g)

def outputs_stats():
    global dfQuery
    global unique_expressions_per_query
    dfQuery = pd.DataFrame(data=queries, columns=['query','type','expression'])
    #print dfQuery

    unique_expressions_per_query = dfQuery.groupby(['expression'])['query'].nunique().sort_values().to_frame()
    unique_expressions_per_query.reset_index(level=0, inplace=True)

    print "Total expressions: {}".format( len(unique_expressions_per_query) )

    with pd.option_context('display.max_rows', None):
        # expressions PER query!! cool
        if args.print_sorted:
            pprint( unique_expressions_per_query.sort_values('expression').to_dict('records') )
        else:
            #print unique_expressions_per_query.to_string()
            pprint( unique_expressions_per_query.to_dict('records') )

if(args.test):
    r = erase_identifier_names(parse(args.test), debug=True)
    print ''.join(token.value for token in r.flatten())
    print transform_statement('test', args.test)
    sys.exit(1)

with open(args.filename) as fh:
    plans = json.load(fh)

for p in plans:
    analyze_outputs(p)

if not args.filter and not args.filter_re:
    outputs_stats()
