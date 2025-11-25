{{ config(
    materialized          = 'incremental',
    incremental_strategy  = 'merge',
    merge_exclude_columns = ['location_pk'],
    unique_key            = ['source_id'],
    schema                = 'aserv',
    tags                  = ["natal"],
) }}

select
gen_random_uuid() location_pk,
a.source_id, a.country,
coalesce(a.county, '__NoCounty__') county,
coalesce(a.state, '__NoState__') state,
a.city, a.timezone, a.latitude, a.longitude,
(now() at time zone 'utc') sys_crt,
null::timestamptz sys_updt
from
{{ ref('w_location') }}  a
