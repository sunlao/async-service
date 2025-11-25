{{ config(
    tags = ['natal'],
) }}

select distinct a.timezone from {{ ref('w_location') }}  a 
EXCEPT
SELECT name FROM pg_timezone_names