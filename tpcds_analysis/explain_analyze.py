#!/usr/bin/env python
import json, argparse
from pprint import pprint
import re
import sys
import pandas as pd

# search for opportunities for predicate pushdown in postgresql query plans

# parse tpcds scaling.dst to pull out scaling properties etc
table_properties = {}
def parse_table_properties():
    #Copy and pasted from scaling.dst:
    #------
    #-- rowcount
    #-- This distribution defines the rowcounts for each table at 
    #-- 6 discrete scaling levels the first (scale=1G) is intended 
    #-- for validation testing
    #-- other values are not valid for publication, but are generated using
    #-- the interpolation method defined for each table
    #-- NOTE: this needs to sync with the definitions in tables.h
    #-- values                     weights
    #-- -------------------------------------------------
    #-- 1. table                1. 1GB rowcount
    #-- 2, multiplier (10^x)       2. 10GB rowcount
    #-- 3. scaling model           3. 100GB rowcount
    #--    (1 = static, 2=linear,     4. 300GB rowcount
    #--    3=logarithmic)          5. 1TB rowcount
    #--                         6. 3TB rowcount
    #--                         7. 10TB rowcount
    #--                         8. 30TB rowcount
    #--                         9. 100TB rowcount
    #--                         10. update percentage
    #------
    def add(name, multiplier, model, *args):
        #only capture the name, multiple and model for now
        model_lookup = {
            -1: '-1'
            , 0: '0'
            ,1: 'static'
            ,2: 'linear'
            ,3: 'logarithmic'
        }
        table_properties[name] = {
            'multiplier': multiplier
            , 'model': model_lookup[model]
            , 'rowcount_10gb': args[1] * (10**multiplier)
            , 'rowcount_1tb': args[4] * (10**multiplier)
            , 'rowcount_100tb': args[8] * (10**multiplier)
        }

    #copy and pasted from scaling.dst
    #--    table       mult     model    1G    10G      100G     300G     1T       3T       10T      30T      100T     upd
    add ("call_center",  0,    3,       3,    12,      15,      18,      21,      24,      27,      30,      30,         0)
    add ("catalog_page", 0,    1,       11718,12000,   20400,   26000,   30000,   36000,   40000,   46000,   50000,      0)
    add ("catalog_returns", 4, 2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("catalog_sales",   4, 2,       16,   160,     1600,     4800,    16000,   48000,   160000,  480000,  1600000,    0)
    add ("customer",     3,    3,       100,  500,     2000,    5000,    12000,   30000,   65000,   80000,   100000,     0)
    add ("customer_address",3, 3,       50,   250,     1000,    2500,    6000,    15000,   32500,   40000,   50000,      0)
    add ("customer_demographics",2, 1,  19208,19208,   19208,   19208,   19208,   19208,   19208,   19208,   19208,      0)
    add ("date_dim",         0,    1,       73049,73049,   73049,   73049,   73049,   73049,   73049,   73049,   73049,      0)
    add ("household_demographics",0,1,  7200, 7200,    7200,    7200,    7200,    7200,    7200,    7200,    7200,       0)
    add ("income_band",  0,    1,       20,   20,      20,      20,      20,      20,      20,      20,      20,         0)
    #--    inventory is a special case derived from item, warehouse, date
    add ("inventory",    -1,   -1,      -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("item",         3,    3,       9,    51,      102,     132,     150,     180,     201,     231,     251,     0)
    add ("promotion",    0,    3,       300,  500,     1000,    1300,    1500,    1800,    2000,    2300,    2500,    0)
    add ("reason",       0,    3,       35,   45,      55,      60,      65,      67,      70,      72,      75,         0)
    add ("ship_mode",    0,    1,       20,   20,      20,      20,      20,      20,      20,      20,      20,         0)
    add ("store",        0,    3,       6,    51,      201,     402,     501,     675,     750,     852,     951,     0)
    add ("store_returns",-1,   2,      -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("store_sales",  4,    2,       24,   240,     2400,    7200,    24000,   72000,   240000,  720000,  2400000,    0)
    add ("time",         0,    1,       86400,86400,   86400,   86400,   86400,   86400,   86400,   86400,   86400,      0)
    add ("warehouse",    0,    3,       5,    10,      15,      17,      20,      22,      25,      27,      30,         0)
    add ("web_page",     0,    3,       30,   100,     1020,    1302,    1500,    1800,    2001,    2301,    2502,     0)
    add ("web_returns",  4,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("web_sales",    3,    2,       60,   600,     6000,    18000,   60000,   180000,  600000,  1800000, 6000000, 0)
    add ("web_site",     0,    3,       15,   21,      12,      21,      27,      33,      39,      42,      48,         0)
    add ("dbgen_version",0,    1,       1,    1,       1,       1,       1,       1,       1,       1,       1,       0)
    #-- source schema tables
    #--    table       mult     model    1G    10G      100G     300G     1T       3T       10T      30T      100T     upd
    add ("s_brand",      2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         10)
    add ("s_customer_address",0,2,      25,   40,      100,     250,     600,     1500,    3250,    4000,    5000,    10)
    add ("s_call_center",0,    2,       1,    1,       1,       1,       1,       1,       1,       1,       1,       100)
    add ("s_catalog",    0,    0,       1,    10,      100,     300,     1000,    3000,    10000,   30000,   100000,     10)
    add ("s_catalog_order", 2, 1,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,      0)
    add ("s_catalog_lineitem",0,1,      -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_catalog_page",  0, 2,       150,  210,     240,     240,     240,     240,     240,     240,     240,     15)
    add ("s_catalog_promotional_item",2,2,-1, -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         10)
    add ("s_catalog_returns",2,2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_category",   2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_class",      2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_company",    2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_customer",   3,    2,       5,    10,      20,      50,      120,     300,     650,     800,     1000,    15)
    add ("s_division",   2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_inventory",  2,    2,       1,    10,      100,     300,     1000,    3000,    10000,   30000,   100000,     0)
    add ("s_item",       2,    2,       5,    7,       10,      13,      15,      18,      20,      23,      25,         50)
    add ("s_manager",    2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_manufacturer",2,   2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_market",     2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_product",    2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_promotion",  0,    2,       5,    7,       10,      13,      15,      18,      20,      23,      25,         50)
    add ("s_purchase",   3,    1,       8,    8,       80,      240,     800,     2400,    8000,    24000,   180000,     0)
    add ("s_purchase_lineitem",2, 2,    -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_reason",     2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_store",      0,    2,       1,    1,       2,       4,       5,       6,       7,       8,       9,       10)
    add ("s_store_promotional_item",2, 2,-1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_store_returns",2,  2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_subcategory",2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_subclass",   2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_warehouse",  0,    2,       1,    1,       1,       1,       1,       1,       1,       1,       1,       100)
    add ("s_web_order",  3,    1,       4,    20,      40,      120,     400,     1200,    4000,    12000,   40000,      0)
    add ("s_web_order_lineitem",2,2,    -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_web_page",   0,    2,       6,    1,       200,       260,       300,       360,       400,       460,       500,       50)
    add ("s_web_promotional_item",2,2,  -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_web_returns",2,    2,       -1,   -1,      -1,      -1,      -1,      -1,      -1,      -1,      -1,         0)
    add ("s_web_site",   0,    2,       1,    1,       1,       1,       1,       1,       1,       1,       1,       50)
    add ("s_zip_to_gmt", 3,    2,       100,  100,     100,     100,     100,     100,     100,     100,     100,     0)
    #-- PSEUDO TABLES, cardinalities, but not actual rowcounts
    #--    table       mult  model 1G    10G      100G  300G  1T    3T    10T      30T      100T     upd
    add ("item_brands",     0,    1,    1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,    0)
    add ("item_classes", 0,    1,    100,  100,  100,  100,  100,  100,  100,  100,  100,     0)
    add ("item_categories", 0,    1,    10,      10,      10,      10,      10,      10,      10,      10,      10,         0)
    add ("divisions",    0,    3,    2,    3,    4,    5,    5,    5,    5,    5,    5,       0)
    add ("companies",    0,    3,       2,    3,    4,    5,    5,    5,    5,    5,    5,       0)
    add ("concurrent_web_sites",0,   3,    2,    3,    4,    5,    5,    5,    5,    5,    5,       0)
    add ("active_cities",   0,     3,    2,    6,    18,      30,      54,      90,      165,  270,  495,     0)
    add ("active_counties", 0,    3,    1,    3,    9,    15,      27,      45,      81,      135,  245,     0)
    add ("active_states",   0,    3,    1,    3,    9,    13,      21,      29,      34,      42,      47,         0)
    pass

def search_top_plans(query_name, top_level_plan):
    scans = search_plans(query_name, [top_level_plan[0]['Plan']])
    return scans

def search_plans(query_name, plans):
    scans = []
    #expecting array
    for p in plans:
        #pprint(p,depth=2)

        #if p['Node Type'] == 'Seq Scan' and 'Filter' in p:
        if re.search('Scan', p['Node Type']): #and 'Filter' in p:
            node_type = p['Node Type']
            scan_type = re.match('(.*) Scan', node_type).groups(1)[0]
            table = None
            if scan_type == 'Seq' or scan_type == 'Index':
                table = p['Relation Name']
                scan_type = 'Seq or Index' #group seq or index scans
            else:
                table = node_type

            table_props = table_properties.get(table, {'model': 'unknown'})

            #print '**** query {} found scan {} with filter over {}'.format(query_name, scan_type, table)
            #print '**** found scan {} with filter over {}'.format(scan_type, table)
            #print '**** found scan {} with filter over {} that grows {}'.format(scan_type, table, table_props['model'])
            #print '**** found scan {} with filter that grows {}'.format(scan_type, table_props['model'])
            #pprint(p,depth=1)
            scans.append({
                "query": query_name
                , "node_type": node_type
                , "scan_type": scan_type
                , 'filtered': 'Filter' in p
                , "table": table
                , "table_growth": table_props.get('model', None)
                , 'rowcount_10gb': table_props.get('rowcount_10gb',None)
                , 'rowcount_1tb': table_props.get('rowcount_1tb', None)
                , 'rowcount_100tb': table_props.get('rowcount_100tb', None)
            })
            pass
        elif 'Filter' in p:
            #print '**** query {} found another node with a filter:'.format(query_name)
            #pprint(p,depth=1)
            pass

        if 'Plans' in p:
            #print '****** recurse plan'
            scans += search_plans(query_name, p['Plans'])

    return scans

def analyze_scans(scans):
    df = pd.DataFrame.from_records(scans)
    #print df

    filtered_vs_unfiltered = df.groupby(['filtered'])

    # overall stats
    unfiltered =  len(filtered_vs_unfiltered.groups[False])
    filtered_len =  len(filtered_vs_unfiltered.groups[True]) 
    total = float(len(df))
    print "Filtered Scans: {} {}%".format( filtered_len, round(filtered_len/total*100,2) )
    print "Unfiltered Scans: {} {}%".format( unfiltered, round(unfiltered/total*100,2) )


    # CTE versus Index/Seq Scans
    print "*** Scan Breakdown:"
    print df.groupby(['scan_type']).count()['filtered']

    # how many sequential or index scans vs CTE scans??
    print "*** Scan Type vs Growth Type of Filtered Scans Breakdown:"
    filtered = df[(df.filtered == True)]
    scan_vs_growth = filtered.groupby(['scan_type', 'table_growth']).count()
    scan_vs_growth_pct = filtered.groupby(['scan_type', 'table_growth']).count() / filtered_len*100
    print scan_vs_growth['filtered']
    print scan_vs_growth_pct['filtered']

    # what's the rowcounts?
    print "**** Row Counts x Usage (i.e. how much data if we ran all of TPC-DS)"
    rowcount_tables = ['rowcount_10gb', 'rowcount_1tb', 'rowcount_100tb']
    print filtered.groupby(['table', 'table_growth']).sum()

    #unique queries
    print "*** unique queries that can benefit from filter pushdown"
    table_scans = filtered[ filtered['scan_type'] == 'Seq or Index' ]
    print  table_scans.groupby(['scan_type']).count()
    print "unique: {}".format( len(table_scans.groupby(['query']).count()) )
    print "total: {}".format( len(df.groupby(['query']).count()) )
 
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for filter pushdown opportunities in postgresql query plans in json format')
    parser.add_argument('files', nargs='+', help='filenames of query plans')
    #parser.add_argument('--output', '-o', help='output file for json')
    #parser.add_argument('--query', '-q', help='print out the query (useful for debugging)', action='store_true')
    args = parser.parse_args()

    parse_table_properties()

    all_scans = []

    for f in args.files:
        with open(f) as fh:
            d = json.load(fh)
        all_scans += search_top_plans(f, d)

    analyze_scans(all_scans)
