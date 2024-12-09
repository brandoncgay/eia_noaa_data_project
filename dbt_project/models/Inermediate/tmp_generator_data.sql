{{ config(
    materialized='view'
) }}

with generator_data as (
select
    UTILITY_ID,
    UTILITY_NAME,
    PLANT_CODE,
    PLANT_NAME,
    STATE,
    COUNTY,
    ARRAY_AGG(distinct TECHNOLOGY) as TECHNOLOGIES,
    ARRAY_AGG(distinct ENERGY_SOURCE_1) as ENERGY_SOURCES
from {{ref("EIA_Generators_Y2023")}}
group by 1,2,3,4,5,6
)

select * from generator_data