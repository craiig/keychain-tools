#!/usr/bin/env python

import argparse
import json
import sys
from pprint import pprint

parser = argparse.ArgumentParser(description='flatten plans')
parser.add_argument('filenames', help='filename of sql query', nargs='+')
args = parser.parse_args()

plan_id_counter = 0
def flatten_plans_recur(filename, plans):
    global plan_id_counter
    allplans = [] 

    for p in plans:
        p['filename'] = filename
        p['plan_id'] = plan_id_counter
        plan_id_counter = plan_id_counter + 1
        if("Plans" in p):
            allplans = allplans + flatten_plans_recur(filename, p["Plans"])
            #reassign plans to be ids
            p["Plans"] = [c['plan_id'] for c in p["Plans"]]

    allplans = allplans + plans
    return allplans

flattened = []
#pprint(args.filenames)
for fn in args.filenames:
    with open(fn) as fh:
        plans = json.load(fh)
        plans = plans[0]["Plan"]
    flattened = flattened + flatten_plans_recur(fn, [plans])

print json.dumps(flattened, indent=1)
#pprint(flattened)
#print "total plans: %s" % (len(flattened))
#print "total plans: %s" % (plan_id_counter)
