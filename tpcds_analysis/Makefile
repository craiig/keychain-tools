ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

build_dir := build/
tpcds_dir := $(shell greadlink -f ../../databricks-tpcds-kit)
tools_dir := $(tpcds_dir)/tools

queries := $(wildcard $(tpcds_dir)/query_templates/query*.tpl)
generated_queries := $(patsubst $(tpcds_dir)/query_templates/%.tpl, build/%.sql, $(queries))
explained_queries := $(patsubst build/%.sql, build/%.json, $(generated_queries))

all: $(generated_queries) $(explained_queries)

#WARNING dsqgen is very sensitive to long paths on the output_dir so we just
# keep it simple and copy from there
build/%.sql: $(tpcds_dir)/query_templates/%.tpl
	mkdir -p $(dir $@)
	cd $(tools_dir) && ./dsqgen -rngseed 12345 -template $(notdir $<) -output_dir ./ -sc 1 -directory $(tpcds_dir)/query_templates/ -dialect netezza
	cd $(tools_dir) && mv query_0.sql $(ROOT)/$@

build/%.json: build/%.sql
	./postgres_explain.py $< > $@

.PHONY: clean
clean:
	-rm -rf build/query*.sql

install:
	pip install --upgrade sqlparse
