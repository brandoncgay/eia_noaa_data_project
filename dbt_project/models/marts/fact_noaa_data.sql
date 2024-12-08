{{ config(
    materialized='table'
) }}

with noaa_data as (
select 
    d.date,
    d.element,
    d.data_value,
    s.latitude,
    s.longitude,
    s.state
from {{ ref('base_bootcamp_raw_noaa_data' )}} d
join {{ ref('noaa_stations')}} s
on d.id = s.id
where d.element in ('TMIN', 'TMAX', 'PRCP', 'SNOW', 'SNWD', 'TSUN', 'WDMV')
and s.state is not null
)

select * from noaa_data