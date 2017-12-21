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

    #canonicalize subplan references
    #what is the difference between SubPlan \d and $2?
    # SubPlan is a plan that has dependencies on other parts of the query
    # InitPlan ($\d)+ references are plans that have no dependencies and can be executed once
    #  InitPlans are as good as constants assuming no updates to the underlying data happens
    #  for our purposes we group them together as one
    sql = re.sub("SubPlan \d+", "subplan_reference", sql)
    sql = re.sub("\$\d+", "subplan_reference", sql)
    return sql

def parse(sql):
    return sqlparse.parse(parser_preprocess(sql))[0]

def erase_identifier_names(node, debug=False):
    global identifier_numbering, id_map
    id_map = {}
    identifier_numbering = 0;
    node = remove_outer_paranthesis(node)
    return erase_identifier_names_recur(node, debug=debug)

def remove_outer_paranthesis(node):
    #remove any outer paranthesis so we can keep it similar
    if type(node) == sqlparse.sql.Statement and len(node.tokens) == 1  and type(node.tokens[0]) == sqlparse.sql.Parenthesis:
        #print 'remove outer: {}'.format(type(node.tokens[0]) == sqlparse.sql.Parenthesis) 
        parans = node.tokens[0]
        node.tokens = [parans.tokens[1]]

    return node
    pass

def erase_identifier_names_recur(node, in_function=False, debug=False):
    # walk each parse node and modify any identifier name into basic name
    global identifier_numbering, id_map
    #only replace identifiers when we are not in a function and it matches the standard column name regex
    if debug:
        print "---> node: {} type: {} tokenlist: {}".format(node, type(node), isinstance(node, sqlparse.sql.TokenList))
        if hasattr(node,'tokens'):
            print "\ttokens: {}".format(node.tokens)
    if type(node) == sqlparse.sql.Identifier and not in_function and re.match("^[0-9A-z_\.]*$", node.value):
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
        node.tokens = [cand]
        pass
    elif type(node) == sqlparse.sql.Token and (node.ttype == sqlparse.tokens.Number.Integer or node.ttype == sqlparse.tokens.Number.Float):
        if debug:
            print 'number: {}'.format(node)
        node.value = 'numeric_constant'

    if isinstance(node, sqlparse.sql.TokenList):
        for n in node:
            #to avoid re-writing parts of identifiers, including any casts, we won't descend into identifiers
            # this is actually preventing a re-write of an expression
            #if type(node) != sqlparse.sql.Identifier:
            erase_identifier_names_recur(n, in_function=type(node)==sqlparse.sql.Function, debug=debug)
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
        , "op": "(<|>|==|<=|>=|=|/|-|\*)"
        , "non_commute_op": "(\|\|)"
        , "text_constant": "'[^']+?'::text"
        #, "function": "[A-z]+\({col}.*?\)"
    }
    # one level of substitution lets us reference other patterns more easily
    for k in r.iterkeys():
        r[k] = r[k].format(**r)


    #o = re.sub("^'.*'::text$", "'.*'::text constant", o) 
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common

    #high level ops
    o = re.sub("{col} ({op}) {col}".format(**r), "col op col", o)
    o = re.sub("{col} ({op}) \({col}\)::numeric".format(**r), "col op col", o)
    o = re.sub("\({col}\)::numeric ({op}) {col}".format(**r), "col op col", o)
    o = re.sub("{col} ({op}) (numeric|text)_constant".format(**r), "col op constant", o)

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
            print inst

        if args.filter and args.filter == out_stmnt:
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
    dfQuery = pd.DataFrame(data=queries, columns=['query','type','expression'])
    #print dfQuery

    unique_expressions_per_query = dfQuery.groupby(['expression'])['query'].nunique().sort_values()

    print "Total expressions: {}".format( len(unique_expressions_per_query) )
    with pd.option_context('display.max_rows', None):
        # expressions PER query!! cool
        print unique_expressions_per_query.to_string()

if(args.test):
    r = erase_identifier_names(parse(args.test), debug=True)
    print ''.join(token.value for token in r.flatten())
    print transform_statement('test', args.test)
    sys.exit(1)

with open(args.filename) as fh:
    plans = json.load(fh)

for p in plans:
    analyze_outputs(p)

if not args.filter:
    outputs_stats()
