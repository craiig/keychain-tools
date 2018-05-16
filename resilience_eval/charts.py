#!/usr/bin/env python
import argparse
import sys, os
import json
import re
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib
from operator import itemgetter

default_hatches = ["/////" , "\\\\\\" , "...." , "xxx" , "------------" , "*" , "+" , "O" , "o" , "-"]
def render_stack_breakdown(test
    , style_name='hatching'
    , hatches = default_hatches
    , custom_style = {}
    , **kwargs #remainder gets passed to pandas plot
    ):
    valid_styles = ['grayscale', 'ggplot', 'fivethirtyeight', 'hatching']
    assert style_name in valid_styles

    if style_name != 'hatching':
        matplotlib.style.use(style_name)
        #matplotlib.style.use('grayscale')
        #matplotlib.style.use('ggplot')
        #matplotlib.style.use('fivethirtyeight')

    style = {
            "axes.grid": True
            ,"axes.axisbelow": True
            ,"legend.fancybox": True
            ,"svg.fonttype": "path"
            ,"figure.subplot.top": 0.985
            ,"figure.subplot.left": 0.0
            ,"figure.subplot.right": 0.999
            ,"figure.subplot.bottom": 0.15
            ,"font.size": 12.0
            }
    for (k,v) in custom_style.iteritems():
        style[k] = v

    for (key,value) in style.iteritems():
        matplotlib.rcParams[key] = value

    #despite the general headache mixing pandas with matplot lib, it's providing a
    # valuable service by rendering the stacked bar charts properly
    if 'figsize' not in kwargs.keys():
        kwargs['figsize'] = (5,3)
    
    stacked = True
    if 'stacked' in kwargs.keys():
        stacked = kwargs['stacked']
        del kwargs['stacked']

    ax = test.plot(kind="bar", colormap="gray_r", stacked=stacked, **kwargs)
    fig = ax.get_figure()
    #fig.set_tight_layout({'pad':0})

    #add hatching
    # http://stackoverflow.com/questions/22833404/how-do-i-plot-hatched-bars-using-pandas
    # needs the long stings of hatches to apply same hatch to all relevant bars
    if style_name == 'hatching':
        print 'adding hatches'
        #hatches = ''.join(h*len(test) for h in hatches)
        density = 1
        bars = ax.patches
        for (i,bar) in enumerate(bars):
            hatch_id = (i / len(test)) % len(hatches)
            bar.set_hatch( hatches[hatch_id] * density )
            bar.set_color([1,1,1])
            bar.set_edgecolor([0.1,0.1,0.1])

        ax.legend(loc='lower right', bbox_to_anchor=(1, 1), ncol=3)
    else:
        ax.legend(loc='lower right', bbox_to_anchor=(1, 1), ncol=5)
        for bar in ax.patches:
            bar.set_edgecolor([0.1,0.1,0.1])

    #fix label rotations
    for label in ax.get_xticklabels():
        label.set_rotation(35)
        label.set_horizontalalignment("right")

    return ax

def overall_compiler_outcomes(o, args):
    results = o['total_compiler_pass_fail']

    names = [ name for name,c in results.iteritems() ]
    names = [re.sub('_-', ' -', n) for n in names]
    cols = ['passes', 'soft_pass', 'soft_fail', 'fails', 'skipped']
    #cols = ['skipped', 'soft_pass', 'fails', 'skipped']

    def get_col(colname):
        return [ c[colname] for name,c in results.iteritems() ]

    data = { name:get_col(name) for name in cols }
    data['name'] = names

    df = pd.DataFrame(index=names, data=data)

    df.sort_values(by=['passes', 'soft_pass', 'soft_fail', 'fails', 'skipped', 'name'], inplace=True)
    df = df[ cols ]
    df.columns = ['pass', 'qualified pass', 'partial fail', 'fail', 'skipped']
    print df

    #ax = render_stack_breakdown(df, style_name='ggplot')
    ax = render_stack_breakdown(df, style_name='hatching')
    ax.set_ylabel("Resilience Outcomes")
    ax.set_xlabel("")

    path = os.path.join(args.output_dir, 'overall_compiler_outcomes.pdf')
    plt.savefig(path, bbox_inches='tight', dpi=300)
    path = os.path.join(args.output_dir, 'overall_compiler_outcomes.png')
    plt.savefig(path, bbox_inches='tight', dpi=300)

def main():
    parser = argparse.ArgumentParser(description='generate charts based on resilience outcome')
    parser.add_argument('--output_dir', '-o', help='output dir', required=True)
    parser.add_argument('--file', '-f', help='resilience outcome to load', required=True)
    args = parser.parse_args()

    with open(args.file) as fh:
        outcome = json.load(fh)

    overall_compiler_outcomes(outcome, args)

if __name__ == "__main__":
    main()
