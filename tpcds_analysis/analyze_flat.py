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
parser.add_argument('--csv', '-c', help='csv file to dump')
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

def erase_identifier_names(node, stats, debug=False):
    global identifier_numbering, id_map
    id_map = {}
    identifier_numbering = 0;
    node = remove_outer_paranthesis(node)
    if args.test:
        pprint_tree(node)
    return erase_identifier_names_recur(node, stats, debug=debug)

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

def erase_identifier_names_recur(node, stats, in_function=False, debug=False):
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
        func_renames = {
                'avg': 'agg'
                ,'sum': 'agg'
                ,'max': 'agg'
                ,'min': 'agg'
                ,'count': 'agg'
                ,'stddev_samp': 'agg'
                ,'round': 'func'
                ,'GROUPING': 'agg'
        }
        if node.value in func_renames:
            if debug:
                print "func replacement"
            #disable coding functions for now, they are the same as expressions?
            #stats['codes'].append( func_renames[node.value] )
            node.tokens = [sqlparse.sql.Token(sqlparse.tokens.Name, func_renames[node.value])]
    elif type(node)==sqlparse.sql.Function and node.tokens[0].value == 'COALESCE':
        #transform coalesce into just the identifier reference (first argument)
        # this is OK for our analysis because coalesce is written in a very specific way
        if debug:
            print "coalesce node.tokens: {} node.tokens[1].tokens: {}".format(node.tokens, node.tokens[1].tokens)
        cand = node.tokens[1].tokens[1]
        if(type(cand) == sqlparse.sql.IdentifierList):
            if debug:
                print 'identifier list tokens: {}'.format(cand.tokens)
            #sometimes an expression list can be parsed as an identifier list, sometimes not
            # tests cases:
            #   "COALESCE(identifier0, '0'::numeric)"
            #   "sum(COALESCE((store_sales.ss_sales_price * (store_sales.ss_quantity)::numeric), '0'::numeric))"
            # when it's an identifier list we may need to add a parenthesis
            # node to preserve order of ops for other parts of this analysis
            #cand = cand.tokens[0]
            cand = [ #sqlparse.sql.Token(sqlparse.tokens.Punctuation, '('),
                    cand.tokens[0]
                    #sqlparse.sql.Token(sqlparse.tokens.Punctuation, ')')
                    ]
            node.tokens = cand
        else:
            node.tokens = [cand]
        if debug:
            print "coalesce replacement candidate: {} type: {}".format( cand, type(cand))
        # this transform can mess with ordering of operations for things inside the coalesce statement
        # we actually need to do the INVERSE and make sure a parenthesis gets added if it not already there
        # test case: 'round(((ss.ss_qty / COALESCE((ws.ws_qty + cs.cs_qty), '1'::bigint)))::numeric, 2)'
        #if(cand.tokens[0].value == '(' and cand.tokens[-1].value == ')'):
            #if debug:
                #print "trimming parenthesis from coalesce in: {} out: {}".format(cand.tokens, cand.tokens[1:-1])
            #cand.tokens = cand.tokens[1:-1]
        #TODO coalesce needs to trip column identifier stuff too
        #since we removed coalesce we can mark ourseles as not being in a function anymore
        next_in_function = False
        pass
    elif isinstance(node, sqlparse.sql.TokenList) and len(node.tokens) == 3 and node.tokens[1].value == '::':
        #detect constants and expression casts
        # rewrite constants and remove expression casts
        left = node.tokens[0]
        right = node.tokens[2]
        if args.test:
            print 'cast detected left:{} right{}'.format(type(left), type(right))
        if type(left) == sqlparse.sql.Parenthesis:
            # [<Parenthesis '(((sr_...' at 0x10577A2D0>, <Punctuation '::' at 0x1057989A8>, <Builtin 'numeric' at 0x105798A10>
            if args.test:
                print "removing expression cast: expression: {}".format(left)
            node.tokens = [left]
        elif type(right) == sqlparse.sql.Token:
            # [<Integer '-1' at 0x106188870>, <Punctuation '::' at 0x1061888D8>, <Builtin 'integer' at 0x106188940>]
            # [<Keyword 'NULL' at 0x10C3B4A78>, <Punctuation '::' at 0x10C3B4AE0>, <Builtin 'text' at 0x10C3B4B48>]
            #use a type mapping to throw an error if we have a unhandled type
            type_map = {
                    'integer': 'numeric',
                    'numeric': 'numeric',
                    'bigint': 'numeric',
                    'text': 'text',
                    'date': 'date',
                    'timestamp': 'date'
                    }
            name = "{}_constant".format(type_map[right.value])
            node.tokens = [sqlparse.sql.Token(sqlparse.tokens.Name, name)]
            if args.test:
                print "rewrote const cast as {}".format(name)

    elif type(node) == sqlparse.sql.Token and (node.ttype == sqlparse.tokens.Number.Integer or node.ttype == sqlparse.tokens.Number.Float):
        #detect certain numeric constants that the parser picks up
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
            erase_identifier_names_recur(n, stats, in_function=next_in_function, debug=debug)
    if debug:
        print "<---"

    # since sqlparse stores a string value for each node
    # since we've changed the name we need to rebuild it back up
    oldval = node.value
    return node

def pprint_tree(node):
    def pprint_tree_recur(node):
        ret = {
            'type': type(node)
            , 'value': node.value
            , 'token_list': isinstance(node, sqlparse.sql.TokenList)
        }
        if(isinstance(node, sqlparse.sql.TokenList)):
            ret['tokens'] = [ pprint_tree_recur(n) for n in node.tokens ]     
        return ret

    #just flip this into something pprint will handle
    pprint(pprint_tree_recur(node))

def stats_keys():
    return stats_defaults().keys()

def stats_init_defaults(s):
    for k,v in stats_defaults().iteritems():
        if k not in s:
            s[k] = v;
    return s

def stats_defaults():
    return {'query': '',
            'type': '',
            'expression': '',
            'columns_count': 0,
            'constants_count': 0,
            'aggregates_count': 0,
            'operators_count': 0,
            'conditionals_count': 0,
            'codes': []
        } 

def compute_stats(node, transformed_statement, stats):
    #pprint_tree(node)
    stats['columns_count'] = len(id_map)
    
    constants = re.findall('[A-z]+_constant', transformed_statement)
    stats['constants_count'] = len(constants)
    aggregates = re.findall('agg\(', transformed_statement, re.IGNORECASE)
    stats['aggregates_count'] = len(aggregates)
    conditionals = re.findall('case ', transformed_statement, re.IGNORECASE)
    stats['conditionals_count'] = len(conditionals)

def transform_statement(ty, stmnt, stats, debug=False):
    o = stmnt
    orig_node = erase_identifier_names(parse(o), stats, debug=debug)
    o = str(orig_node)

    r = {
        #"col" : "[0-9A-z_\.]+"
        "col" : "identifier[0-9]+"
        ,"constant": "[A-z]+_constant"
        ,"col_or_constant": "({col}|{constant})"
        , "op": "(<|>|==|<=|>=|=|/|-|\*|<>|\+|OR|AND)"
        , "math_op": "(/|-|[^\(]\*[^\)]|\+)"
        , "comparison_op": "(<|>|==|<=|>=|=|<>)"
        , "logical_op": "(OR|AND)"
        , "non_commute_op": "(\|\|)"
        , "text_constant": "'[^']+?'::text"
        , "date_constant": "'[^']+?'::date"
        #, "function": "[A-z]+\({col}.*?\)"
    }
    # one level of substitution lets us reference other patterns more easily
    for k in r.iterkeys():
        r[k] = r[k].format(**r)


    #the process of coding we're doing here is to directly map expressions into 
    # what we can test will test with regard to the compiler optimizations, so we
    # write regexes that will match expression patterns and output a CODE for each
    # compiler optimization that can be tested

    codes = {
            #'{op}': 'binary_op' #variant type 2
            '{constant}': 'constant_folding' #variant type 2
            , 'case.*?when': 'conditional' #variant type 3, reordering and equivalencies

            #left over categories
            #, '{col} {op} {col}': 'col_op_col'
            #, '{col} {op} {constant}': 'col_op_constant'
            #, 'agg\(case when' : 'aggregate_conditional'

            #further classify some operands (not part of the variant types)
            , '{math_op}': 'math_op'
            , '{comparison_op}': 'comparison_op'
            , '{logical_op}': 'logical_op'
            #, '{non_commute_op}': 'non_commute_op'

            , 'ANY\s*\(': 'array_any' #this is actually a compact if/or clause
            , 'ALL\s*\(': 'array_all'

            # these patterns don't correspond to a compiler feature but we assign
            # a code here so that every expression gets a code, 
            # actually we don't need to do this
            #, '^{col}$': 'single_column'
            #, 'rank\(\) OVER \(\?\)': 'columnless_aggregate'
            #, '^{col} is null$': 'column_to_null_compare'
            #, '^{col} is not null$': 'column_to_null_compare'
    }
    for (regexp,code) in codes.iteritems():
        if re.search(regexp.format(**r), o, re.IGNORECASE):
            stats['codes'].append(code)

    #some control flow patterns
    # i think a few conditional aggregations would be good to add to a test
    #o = re.sub("^agg\(CASE WHEN \(.*\) THEN numeric_constant ELSE numeric_constant END\)$", "conditional aggregate", o)
    #o = re.sub("^agg\(CASE WHEN \(.*\) THEN {col} ELSE numeric_constant END\)$".format(**r), "conditional aggregate", o)
    #o = re.sub("agg\(CASE WHEN \(.*\) THEN .*? ELSE .*? END\)".format(**r), "conditional aggregate", o) #catch all to isolate this category entirely

    #o = re.sub("^\(([^\(\)]*?)\)$", "\\1", o) #eliminate outer parenthesis as long as there are no inner paranthesis
        #o = re.sub("^round\(\([0-9A-z_\.]*? / [0-9A-z\.]*?\), \d+\)$", "rounded_division", o)

    #o = re.sub("^{col} ({op}) {col}$".format(**r), "col1 \\1 col2", o)
    #o = re.sub("{col} ({op}) {col}".format(**r), "col1 \\1 col2", o)
    #o = re.sub("^{col} ({non_commute_op}) {col}$".format(**r), "col1 \\1 col2", o)

    #o = re.sub("{function}".format(**r), "col1 \\1 col2", o)
    #o = re.sub("{col} ({op}) {function}".format(**r), "col1 \\1 col2", o)

    #unique and sorted
    stats['codes'] = list(set(stats['codes']))
    stats['codes'].sort()

    compute_stats(orig_node, o, stats)
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
        stats = {
            'query': query,
            'type': ty,
        }
        #init other columns to zero
        stats = stats_init_defaults(stats)
        try: 
            out_stmnt = transform_statement(ty,in_stmnt,stats)
            stats['expression'] = out_stmnt
        except Exception as inst:
            print "exception parsing statement: {}".format(in_stmnt)
            raise

        if args.filter and args.filter == out_stmnt:
            print in_stmnt
        if args.filter_re and re.match(args.filter_re, out_stmnt):
            print in_stmnt
 
        queries.append(stats)

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
    dfQuery = pd.DataFrame(data=queries, columns=stats_keys())

    unique_expressions_per_query = dfQuery.groupby(['expression'])['query'].nunique().sort_values().to_frame()
    unique_expressions_per_query.reset_index(level=0, inplace=True)

    #sum up numeric stats across expressions? queries?
    # sum up across expressions and sort by number of identifiers
    # let's take the PER expression stats and I think finally it's time to get
    # these out of pandas
    #pprint( dfQuery.groupby(['expression'])['query'].sum().sort_values('expression').to_dict('records').sort_values('expression').to_dict('records') )

    print "Total expressions: {}".format( len(unique_expressions_per_query) )

    if args.csv:
        with open(args.csv, 'w+') as fh:
            dfQuery.to_csv(fh, index=False)

    with pd.option_context('display.max_rows', None):
        if args.print_sorted:
            # expressions PER query!! cool
            pprint( unique_expressions_per_query.sort_values('expression').to_dict('records') )
        else:
            #print unique_expressions_per_query.to_string()
            pprint( unique_expressions_per_query.to_dict('records') )

if(args.test):
    stats = stats_init_defaults({})
    #r = erase_identifier_names(parse(args.test), stats, debug=True)
    #print ''.join(token.value for token in r.flatten())
    print transform_statement('test', args.test, stats, debug=True)
    pprint(stats)
    sys.exit(1)

with open(args.filename) as fh:
    plans = json.load(fh)

for p in plans:
    analyze_outputs(p)

if not args.filter and not args.filter_re:
    outputs_stats()
