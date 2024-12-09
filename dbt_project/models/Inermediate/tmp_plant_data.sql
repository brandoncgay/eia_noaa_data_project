{{ config(
    materialized='view'
) }}

with plant_data as (
select
    UTILITY_ID,
    UTILITY_NAME,
    PLANT_CODE,
    PLANT_NAME,
    STREET_ADDRESS,
    CITY,
    STATE,
    ZIP,
    COUNTY,
    LATITUDE,
    LONGITUDE,
    BALANCING_AUTHORITY_CODE,
    BALANCING_AUTHORITY_NAME
from {{ ref('EIA_Plant_Y2023') }}
where BALANCING_AUTHORITY_CODE is not null
)

select * from plant_data