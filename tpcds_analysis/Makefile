ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

build_dir := build/
tpcds_dir := $(shell greadlink -f ../../databricks-tpcds-kit)
tools_dir := $(tpcds_dir)/tools

queries := $(wildcard $(tpcds_dir)/query_templates/query*.tpl)
generated_queries := $(patsubst $(tpcds_dir)/query_templates/%.tpl, queries/%.sql, $(queries))
explained_queries := $(patsubst queries/%.sql, plans/%.json, $(wildcard queries/*.sql))

all: $(generated_queries) $(explained_queries) flattened.json

#WARNING dsqgen is very sensitive to long paths on the output_dir so we just
# keep it simple and copy from there
queries/%.sql: $(tpcds_dir)/query_templates/%.tpl
	mkdir -p $(dir $@)
	cd $(tools_dir) && ./dsqgen -rngseed 12345 -template $(notdir $<) -output_dir ./ -sc 1 -directory $(tpcds_dir)/query_templates/ -dialect netezza
	cd $(tools_dir) && mv query_0.sql $(ROOT)/$@

plans/%.json: queries/%.sql
	mkdir -p $(dir $@)
	./postgres_explain.py $< -o $@

flattened.json: $(wildcard plans/*.json)
	./flatten_plans.py $^ > $@

.PHONY: clean
clean:
	#-rm -rf build/query*.sql

install:
	pip install --upgrade sqlparse
