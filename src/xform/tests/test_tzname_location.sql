{{ config(
    tags = ['natal'],
) }}

select distinct a.timezone from {{ ref('location') }}  a 
EXCEPT
SELECT name FROM pg_timezone_names