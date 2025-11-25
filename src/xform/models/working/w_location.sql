{{ config(
    schema="working",   
    materialized="table",
    tags=["natal"]
) }}

select
source_id, country, state, county, city, timezone, latitude, longitude
from(
	select
	source_id, country, state, county, city, timezone, latitude, longitude,
	row_number()over(partition by country, state, county, city order by source_id)row_num
	from(
		select distinct 
		a.geonameid::bigint source_id, a.asciiname city,
		b.name country,
		coalesce(e.name, c.name) as state,
		d.name county,
		a.timezone,
		a.latitude::float latitude, 
		a.longitude::float longitude
		from
        {{ source('raw','cities') }} a
			join {{ source('raw','iso_country') }} b on a.country_code = b.code
			left join {{ source('raw','admin1') }} c on a.country_code||'.'||a.admin1_code = c.code
			left join {{ source('raw','admin2') }} d on a.country_code||'.'||a.admin1_code||'.'||a.admin2_code = d.code
			left join {{ source('raw','iso_subdivision') }} e on a.country_code||'-'||a.admin1_code = e.code  
		where
		a.timezone != ''
	)
)
where 
row_num = 1