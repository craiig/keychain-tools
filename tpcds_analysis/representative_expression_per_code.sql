COPY ( -- prepare for CSV
-- unnested_code_expressions gives a representative from each variant category
with unnested_code_expressions as (
	with sub_unranked as (
		select
		unnest(regexp_replace(regexp_replace(codes,'\[','{'), '\]','}')::text[]) as code
		, expression
		, count(distinct query) as num_queries_appears
		from hls_research.tpcds_expressions
		group by code, expression
	)
	, sub as (
		select
		*
		-- we pick the most used expression, and if there is a tie we take the
		-- shortest one in length.  row_number() is used instead of rank() to
		-- ensure we pick one result.  rank can return multiple entries if the
		-- sort order puts multiple rows in the same order
		, row_number() over (partition by code order by num_queries_appears desc, char_length(expression) asc) as rank
		from sub_unranked
	)
	, code_stats as (
		select
		unnest(regexp_replace(regexp_replace(codes,'\[','{'), '\]','}')::text[]) as code
		, count(distinct query) as num_queries_code_appears
		from hls_research.tpcds_expressions
		group by code
	)
	select 
	sub.*
	, code_stats.num_queries_code_appears
	from sub join code_stats on sub.code=code_stats.code
	where sub.rank = 1
	order by sub.code, num_queries_appears desc, char_length(expression) asc	
)
select * from unnested_code_expressions

-- output csv
) --close copy query
	to stdout
	with csv header
