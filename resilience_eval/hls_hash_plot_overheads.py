#!/usr/bin/env python
import argparse
import sys, os
import json
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib

def hls_plot(df, args):
    #plot data, spin off into different function later
     print df

     ax = df.plot(kind='scatter', x='bytes', y='took_ns', c='compiler')
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
