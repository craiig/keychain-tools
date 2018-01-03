COPY ( -- prepare for CSV
with expressions as (
	select 
	expression
	, codes
	, array_agg(distinct query) as queries
	, count(*) as total_occurences
	, count(distinct query) as num_queries_appears
	, max(columns_count) as columns_count
	, max(constants_count) as constants_count
	, max(aggregates_count) as aggregates_count
	, max(conditionals_count) as conditionals_count
	from hls_research.tpcds_expressions
	group by expression, codes
	order by expression asc
)
, breakdown_codes as (
	select
	codes,
	count(*) num_expressions,
	round(count(*) / (select count(*) from expressions)::numeric,2) num_expressions_pct,
	count(*) as total_occurences,
	count(distinct query) as num_queries_appears,
	(array_agg(expression))[1] as first_expression
	-- , array_agg(expression) as expressions
	from hls_research.tpcds_expressions
	group by codes
)
-- breakdown_codes gives a breakdown of all unique combinations of codes, this
-- is a larger corpus but more complex
select * from breakdown_codes

-- output csv
) --close copy query
	to stdout
	with csv header
