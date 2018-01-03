ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

build_dir := build/
tpcds_dir := $(shell greadlink -f ../../databricks-tpcds-kit)
tools_dir := $(tpcds_dir)/tools

queries := $(wildcard $(tpcds_dir)/query_templates/query*.tpl)
generated_queries := $(patsubst $(tpcds_dir)/query_templates/%.tpl, queries/%.sql, $(queries))
explained_queries := $(patsubst queries/%.sql, plans/%.json, $(wildcard queries/*.sql))

all: ${build_dir}/representative_expression_per_code.csv ${build_dir}/representative_expression_per_unique_codes.csv
	cat ${build_dir}/representative_expression_per_code.csv

#WARNING dsqgen is very sensitive to long paths on the output_dir so we just
# keep it simple and copy from there
queries/%.sql: $(tpcds_dir)/query_templates/%.tpl
	mkdir -p $(dir $@)
	cd $(tools_dir) && ./dsqgen -rngseed 12345 -template $(notdir $<) -output_dir ./ -sc 1 -directory $(tpcds_dir)/query_templates/ -dialect netezza
	cd $(tools_dir) && mv query_0.sql $(ROOT)/$@

plans/%.json: queries/%.sql
	mkdir -p $(dir $@)
	./postgres_explain.py $< -o $@

${build_dir}/representative_expression_per_code.csv: ./representative_expression_per_code.sql ${build_dir}/csv_loaded
	psql -f $< > $@

${build_dir}/representative_expression_per_unique_codes.csv: ./representative_expression_per_unique_codes.sql ${build_dir}/csv_loaded
	psql -f $< > $@

${build_dir}/flattened.json: $(wildcard plans/*.json)
	./flatten_plans.py $^ > $@

${build_dir}/expressions.csv: ${build_dir}/flattened.json ./analyze_flat.py
	./analyze_flat.py -f $< -c $@

${build_dir}/csv_loaded: ${build_dir}/expressions.csv
	psql -c 'create schema if not exists hls_research'
	ogr2ogr -f PGDump /vsistdout/ '$<' -lco SCHEMA=hls_research \
		-lco DROP_TABLE=IF_EXISTS -lco CREATE_SCHEMA=OFF -nln tpcds_expressions \
		--config PG_USE_COPY YES \
		| psql -v ON_ERROR_STOP=1
	touch $@

.PHONY: clean
clean:
	-rm  build/*

install:
	pip install --upgrade sqlparse
