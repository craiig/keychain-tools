#!/usr/bin/env python

import psycopg2
import psycopg2.extras
from pprint import pprint
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Explain a TPC-DS SQL Query as Json')
parser.add_argument('filename', help='filename of sql query')
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

cur.execute(query)
r = cur.fetchone()
print json.dumps(r['QUERY PLAN'], indent=1)

cur.close()
