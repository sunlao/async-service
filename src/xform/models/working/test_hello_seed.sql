{{ config(
    schema="working",   
    materialized="table",
    tags=["test"]
) }}

select
a.key, a.value
from 
{{ source('raw', 'hello_seed') }} a
