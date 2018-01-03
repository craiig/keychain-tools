
# TPC-DS Analysis

Analyzes all tpcds expressions for common patterns with respect to syntactic variation.
Outputs a set of expressions used in TPC-DS in two files:
```
build/representative_expression_per_code.csv // the most frequently expression PER code
build/representative_expression_per_unique_codes.csv // the most frequent expression per unique code combinations
```

For ease of investigation, these final output files are included in the git
repo. No need to download and run this repo just to look at the results.

# Coding Procedure and Codes used
I manually examined each statement and wrote down a list of different syntactic
variations that could occur when writing the statement. I used this to build a
simple regular expression matcher to consistently tag all expressions with
these codes. The codes and regexes used are listed
[here.](analyze_flat.py#L301) I did not code expressions that
did not have significant syntactic variation.

Codes I used were:
* constant folding
* conditional operations
* array any comparisons
* math operations
* comparison operations
* logical operations

# Requirements

1. Sqlparse: `pip install sqlparse` used to analyze the expressions
2. A running postgresql database that you can connect to from the terminal via
   psql. [Postgres.app](https://postgresapp.com/) is recommended for macOS.
3. GDAL library for ogr2ogr: `brew install gdal` used for importing csv to sql
   for final analysis.
4. If you wish to regenerate the TPCDS queries, the TPCDS toolkit must be
   installed and the Makefile variable `tpcds_dir` must point to it. A macOS
   compatible TPCDS distribution is available
   [here](https://github.com/databricks/tpcds-kit).

# Usage
* Run the expression analysis: `make clean && make`
* Re-analyze the TPCDS queries with Postgres: `rm plans/*.json && make`
* Re-generate the queries, and reanalzye: `rm queries*.sql && make`
