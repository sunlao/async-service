{{ config(
    schema="working",
    materialized="table",
    tags=["test"]
) }}

select
source_word, source_time, sys_source_hash
from
{{ source('raw', 'hello_test_api') }} a
