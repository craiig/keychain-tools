#!/usr/bin/env python
import argparse
import sys, os
import json
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib

def hls_overheads(outcomes, args):
    summary = []
    for o in outcomes:
        s = {
            "name": o['closureName']
            , 'took_ns': o['took_ns']
            , 'took_bytecode_ns': o['bytecode']['took_ns']
            , 'took_primitives_ns': o['primitives']['took_ns']
        }
        bytecode_length = 0
        primitive_length = 0
        #count length of bytecode
        for t in o['bytecode']['trace']:
            #pprint(t)
            #pprint( t['bytecode'])
            bytecode_length += len(t['bytecode'])

        if o['primitives']['hashed_bytes'] != '':
            #print 'primitives added {}'.format( hb_len )
            hb = o['primitives']['hashed_bytes']
            hb_len = len(hb.split(','))
            primitive_length += hb_len

        #assert( o['primitives']['hashed_bytes'] == '' )
        s['bytes'] = bytecode_length + primitive_length
        s['bytes_primitive'] = primitive_length
        s['bytes_bytecode'] = bytecode_length

        summary.append(s)

    df = pd.DataFrame(summary)

    #fdf = df.loc[df['took_ns'] >= 2e8 ]
    #print fdf
    df.to_csv( os.path.join(args.output_dir, 'hash_overhead.csv'))

    #plot data, spin off into different function later
    # ax = df.plot(kind='scatter', x='bytes', y='took_ns')
    # path = os.path.join(args.output_dir, 'hashing_time.pdf')
    # plt.savefig(path, bbox_inches='tight', dpi=300)

def main():
    parser = argparse.ArgumentParser(description='read HLS json traces and output some stats')
    parser.add_argument('--output_dir', '-o', help='output dir', required=True)
    parser.add_argument('--files', '-f', help='hls traces to summarize', required=True, nargs='+')
    args = parser.parse_args()

    outcomes = [json.load(open(f)) for f in args.files]

    hls_overheads(outcomes, args)

if __name__ == "__main__":
    main()
