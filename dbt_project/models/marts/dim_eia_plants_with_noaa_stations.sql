{{ config(
    materialized='table'
) }}

with plant_gen_joined as (
select
    p.UTILITY_ID,
    p.UTILITY_NAME,
    p.PLANT_CODE,
    p.PLANT_NAME,
    p.STREET_ADDRESS,
    p.CITY,
    p.STATE,
    p.ZIP,
    p.COUNTY,
    p.LATITUDE,
    p.LONGITUDE,
    p.BALANCING_AUTHORITY_CODE,
    p.BALANCING_AUTHORITY_NAME,
    g.TECHNOLOGIES,
    g.ENERGY_SOURCES,
    s.STATION_ID,
    s.DISTANCE_M
from {{ref("tmp_plant_data")}} p
join {{ref("tmp_generator_data")}} g
on g.PLANT_CODE = p.PLANT_CODE
join {{ref("tmp_plants_with_nearest_station")}} s
on p.PLANT_CODE = s.PLANT_CODE
)

select * from plant_gen_joined