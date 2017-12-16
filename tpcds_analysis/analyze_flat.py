#!/usr/bin/env python

import argparse
import json
import sqlparse
import sys
from pprint import pprint
from collections import Counter
import re

parser = argparse.ArgumentParser(description='analyze flattened plans')
parser.add_argument('filename', help='filename of plans')
args = parser.parse_args()

with open(args.filename) as fh:
    plans = json.load(fh)

###
identifier_numbering = 0;
id_map = {}
def erase_identifier_names(node):
    global identifier_numbering, id_map
    identifier_numbering = 0
    id_map = {}
    return erase_identifier_names_recur(node)

def erase_identifier_names_recur(node, in_function=False):
    # walk each parse node and modify any identifier name into basic name
    #TODO identifier map
    global identifier_numbering, id_map
    if type(node) == sqlparse.sql.Identifier and not in_function:
        if node.value not in id_map:
            name = 'identifier{}'.format(identifier_numbering)
            id_map[node.value] = name
            identifier_numbering = identifier_numbering + 1
        else:
            name = id_map[node.value]
        node.tokens = [sqlparse.sql.Token(sqlparse.tokens.Name, name)]

    for n in node:
        if isinstance(n, sqlparse.sql.TokenList):
            erase_identifier_names_recur(n, type(node)==sqlparse.sql.Function)

    # since sqlparse stores a string value for each node
    # since we've changed the name we need to rebuild it back up
    oldval = node.value
    return node

def transform_statement(ty, stmnt):
    o = stmnt
    o = str(erase_identifier_names(sqlparse.parse(o)[0]))
    return o

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

    o = re.sub("::bpchar", "::text", o) # synonynms for the same type

    o = re.sub("^[0-9A-z_\.]*$", "column_ref", o)
    o = re.sub("\([0-9A-z_\.]*\)", "(column_ref)", o)
    #o = re.sub("^'.*'::text$", "'.*'::text constant", o) 
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common
    o = re.sub("{text_constant}".format(**r), "text_constant", o) #pretty common

    o = re.sub("^\((.*?)\)$", "\\1", o) #eliminate outer parenthesis
    #o = re.sub("^sum\([0-9A-z_\.]*\)$", "sum(column)", o) #explicitly match sum
    #o = re.sub("^avg\([0-9A-z_\.]*\)$", "avg(column)", o) 
    #o = re.sub("^max\([0-9A-z_\.]*\)$", "max(column)", o) 
    #o = re.sub("^substr\([0-9A-z_\.]*\)$", "substr(column)", o) 

    o = re.sub("^round\(\([0-9A-z_\.]*? / [0-9A-z\.]*?\), \d+\)$", "rounded_division", o)

    o = re.sub("^{col} ({op}) {col}$".format(**r), "col1 \\1 col2", o)
    o = re.sub("{col} ({op}) {col}".format(**r), "col1 \\1 col2", o)
    o = re.sub("^{col} ({non_commute_op}) {col}$".format(**r), "col1 \\1 col2", o)

    #o = re.sub("{function}".format(**r), "col1 \\1 col2", o)
    #o = re.sub("{col} ({op}) {function}".format(**r), "col1 \\1 col2", o)
    return o

outputs = Counter()
all_output_cols = 0;
def analyze_outputs(p):
    global outputs
    global all_output_cols

    def process_statement(ty, stmnt):
        global outputs
        global all_output_cols
        # TODO ignore some nodes to avoid 'over counting'
        # because basic col outputs are very high
        #transform outputs
        stmnt = transform_statement(ty,stmnt)
        outputs[stmnt] += 1
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
#r = erase_identifier_names(sqlparse.parse(test)[0])
#print ''.join(token.value for token in r.flatten())
#print transform_statement('test', test)
#sys.exit(1)

for p in plans:
    analyze_outputs(p)


outputs_stats()
