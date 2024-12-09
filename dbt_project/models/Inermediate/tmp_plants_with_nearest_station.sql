{{ config(
    materialized='view'
) }}

with plant_distance_to_nearest_station as (
select
    PLANT_CODE,
    MIN(DISTANCE_M) as DISTANCE_M
from {{ ref("stations_with_nearest_plant") }} 
group by 1
),

plants_with_nearest_station as (
select
    a.PLANT_CODE,
    b.ID as STATION_ID,
    a.DISTANCE_M
from plant_distance_to_nearest_station a
join stations_with_nearest_plant b
on a.plant_code = b.plant_code and a.distance_m = b.distance_m
)

select * from plants_with_nearest_station