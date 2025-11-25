{{ config(
    tags = ['natal'],
    severity = 'warn'
) }}

select * from {{ ref('w_location_bad') }}  a 
