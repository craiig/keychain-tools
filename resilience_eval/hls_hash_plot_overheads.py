#!/usr/bin/env python
import argparse
import sys, os
import json
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.markers

def hls_plot(df, args):
    #plot data, spin off into different function later
    #print df

    #fdf = df.loc[df['took_ns'] >= 3e8 ]
    matplotlib.style.use('grayscale')

    df['took_ns'] = df['took_ns'] / float(1e6)

    #filter out cached items
    if 'hash_cache_hits' in df:
        df = df.loc[df['hash_cache_hits'] == 0]
    #filter out dat from tpc-ds, we'll present it differently
    df = df.loc[df['compiler'].notnull()]

    #print(df)
    #sys.exit(1)

    # on investigation with tableau found that the other factor is the number of 
    #  functions hashed, in addition to bytes and data
    groups = []
    groups.append( (df.loc[df['functions_visited'] < 10], '< 10') )
    groups.append( (df.loc[ (df['functions_visited'] >= 10) & (df['functions_visited']<30) ], '10-30') )
    groups.append( (df.loc[ (df['functions_visited'] >= 30) & (df['functions_visited']<50) ], '30-50') )
    groups.append( (df.loc[ (df['functions_visited'] >= 50) & (df['functions_visited']<70) ], '50-70') )
    groups.append( (df.loc[ (df['functions_visited'] >= 70) & (df['functions_visited']<90) ], '70-90') )
    groups.append( (df.loc[df['functions_visited'] > 90], '> 90 ') )

    markers = matplotlib.markers.MarkerStyle.filled_markers
    markers = ['o', "^", "s", "P", "X", "H"]

    #plt.tight_layout()
    #plt.figure(figsize=(1,1))
    fig, ax = plt.subplots(figsize=(4,2.5), tight_layout={'pad':0})
    plt.xticks([0,10000,20000,30000])
    #fig, ax = plt.subplots(figsize=(4,2.5), constrained_layout={'pad':0})
    for idx,g in enumerate(groups):
        df = g[0]
        print "****"
        print g[1]
        print g[0]
        print len(df)
        print "****"
        if len(df) > 0:
            #ax = g[0].plot(kind='scatter', x='bytes', y='took_ns', label=g[1])
            ax.scatter(df.bytes, df.took_ns, s=100, label=g[1], marker=markers[idx],
                    edgecolor='grey')#, linewidth=0.1)
    
    ax.set_ylabel("Time (ms)")
    ax.set_xlabel("Bytes Hashed")
    ax.legend(loc='lower right', bbox_to_anchor=(1, 1), ncol=3, title="Functions Hashed")

    plt.ylim(ymin=0,ymax=400)
    plt.xlim(xmin=0)

    path = os.path.join(args.output_dir, 'hashing_time.pdf')
    plt.savefig(path, bbox_inches='tight', dpi=300)

def main():
    parser = argparse.ArgumentParser(description='read HLS hash summary results and plot to pdf')
    parser.add_argument('--csv', '-c', help='csv path', required=True)
    parser.add_argument('--output_dir', '-o', help='output dir', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    hls_plot(df, args)

if __name__ == "__main__":
    main()
