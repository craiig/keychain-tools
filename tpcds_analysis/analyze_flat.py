#!/usr/bin/env python

import argparse
import json
import sqlparse
import sys
from pprint import pprint
from collections import Counter
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
#   binary operations, disregarding operator

###
identifier_numbering = 0;
id_map = {}

def parser_preprocess(sql):
    # needed because sql parse does not recognize bpchar as a built-in
    sql = re.sub("::bpchar", "::text", sql) # synonynms for the same type
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
    #TODO identifier map
    global identifier_numbering, id_map
    #only replace identifiers when we are not in a function and it matches the standard column name regex
    if debug:
        print "---> node: {} type: {} tokenlist: {}".format(node, type(node), isinstance(node, sqlparse.sql.TokenList))
        if hasattr(node,'tokens'):
            print "\ttokens: {}".format(node.tokens)
    if type(node) == sqlparse.sql.Identifier and not in_function and re.match("^[0-9A-z_\.]*$", node.value):
        if node.value not in id_map:
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
        "col" : "[0-9A-z_\.]+"
        , "op": "(<|>|==|<=|>=|=)"
        , "non_commute_op": "(\|\|)"
        #, "binary_op": "{col} ({op}) {col}"
        , "text_constant": "'[^']+?'::text"
        #, "function": "[A-z]+\({col}.*?\)"
    }
    # one level of substitution lets us reference other patterns more easily
    for k in r.iterkeys():
        r[k] = r[k].format(**r)


    #o = re.sub("^'.*'::text$", "'.*'::text constant", o) 
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common

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

outputs = Counter()
all_output_cols = 0;
def analyze_outputs(p):
    global outputs
    global all_output_cols

    def process_statement(ty, in_stmnt):
        global outputs
        global all_output_cols
        # TODO ignore some nodes to avoid 'over counting'
        # because basic col outputs are very high, (or we just don't report it in that way)
        #transform outputs
        out_stmnt = transform_statement(ty,in_stmnt)

        if args.filter and args.filter == out_stmnt:
            print in_stmnt
 
        outputs[out_stmnt] += 1
        all_output_cols = all_output_cols + 1

    #what are the column transformations?
    if "Output" in p:
        for o in p['Output']:
            process_statement('output',o)
            pass

    if "Filter" in p:
        #print p['Filter']
        process_statement('filter',p['Filter'])
        pass

    for k in p.get("Group Key", []):
        process_statement('group', k)
        pass

    def flatten_group_sets(gsets):
        for gs in gsets:
            for gks in gs['Group Keys']:
                for k in gks:
                    yield k

    if("Grouping Sets" in p):
        groups = [item for item in flatten_group_sets(p['Grouping Sets'])]
        for g in groups:
            process_statement('group', g)

def outputs_stats():
    print "total output columns: %s" % (all_output_cols)
    print "total unique cols after post-proessing: {}".format(len(outputs))
    pprint( outputs.most_common(len(outputs)) )

# testing the sql parse identifier erasure
#test = "(catalog_sales.cs_ext_sales_price - COALESCE(catalog_returns.cr_return_amount, 0.0))"
#test = "(item_1.i_category = 'Books'::bpchar)"
#r = erase_identifier_names(sqlparse.parse(test)[0])
#print ''.join(token.value for token in r.flatten())
#print transform_statement('test', test)
#sys.exit(1)

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
