#!/usr/bin/env python

import psycopg2
import psycopg2.extras
from pprint import pprint
import sys
import json
import argparse
import re

parser = argparse.ArgumentParser(description='Explain a TPC-DS SQL Query as Json')
parser.add_argument('filename', help='filename of sql query')
parser.add_argument('--output', '-o', help='output file for json')
parser.add_argument('--query', '-q', help='print out the query (useful for debugging)', action='store_true')
args = parser.parse_args()

with open(args.filename) as fh:
    to_explain = fh.read()

with open('./tpcds.sql') as fh:
    tpcds_schema = fh.read()

conn = psycopg2.connect("")
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

query = """
{schema}

EXPLAIN (format json, verbose)
{query}
""".format(schema=tpcds_schema, query=to_explain)

if(args.query):
    print query
    sys.exit(0)

cur.execute(query)
r = cur.fetchone()

if(args.output != None):
    with open(args.output, "w+") as fh:
        json.dump(r['QUERY PLAN'], fh, indent=1)
else:
    print json.dumps(r['QUERY PLAN'], indent=1)

cur.close()
