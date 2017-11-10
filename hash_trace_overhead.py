#!/usr/bin/env python

# metric goals:
# hash misses / hits
# total overall hashing time ( outlier identification? )
#   help report overheads
# search for similar primitive hashes with tree differences?
#  help to evaluate if a primitive cache would be reasonable (if possible)
#
#  line to remove prefixed text entirely:
#   grep -i "Hashing trace" driver.log | sed -n -e 's/^.*Hashing trace: //p' > hashing_trace.json 

import sys, json, re

def parse_line(line):
    # two ways of parsing: either parse the whole line as json (if the traces
    # have already been stripped from the logs) or it contains some prefix text
    # that we want to shed, so we drop that first and parse the remainder (TODO
    # do verification that the json we pulled was actually an HLS trace, at the
    # moment nothing else seems to be outputting json in the driver logs)
    parsed = None
    try:
        parsed = json.loads(line)
    except ValueError as e:
        # strip everthing up to the first json object/array character
        fixed = re.sub(r'^.*?([{\[])', '\\1', line)
        try: 
            parsed = json.loads(fixed)
        except ValueError as e:
            #ignore error, this line is likely not a valid json
            pass

    return parsed

# overhead analysis
overall_time = 0
bytecode_time = 0
primitives_time = 0
def overhead_line(j):
    global overall_time
    global bytecode_time
    global primitives_time
    overall_time = overall_time + j['took_ns']
    bytecode_time = bytecode_time + j['bytecode']['took_ns']
    primitives_time = primitives_time + j['primitives']['took_ns']
    pass

def overhead_finalize():
    print "overall HLS overhead: %s" % overall_time
    print "bytecode HLS overhead: %s" % bytecode_time
    print "primitives HLS overhead: %s" % primitives_time
    pass

# main event processing loop
for line in sys.stdin:
    j = parse_line(line)
    if j:
        #print j['took_ns']
        overhead_line(j)

overhead_finalize()
