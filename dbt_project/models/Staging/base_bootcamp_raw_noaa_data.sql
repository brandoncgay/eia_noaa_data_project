{{ config(
    materialized='view'
) }}

with source as (
      select * from {{ source('bootcamp', 'raw_noaa_data') }}
),
renamed as (
    select
        {{ adapter.quote("ID") }},
        {{ adapter.quote("DATE") }},
        {{ adapter.quote("ELEMENT") }},
        {{ adapter.quote("DATA_VALUE") }},
        {{ adapter.quote("M_FLAG") }},
        {{ adapter.quote("Q_FLAG") }},
        {{ adapter.quote("S_FLAG") }},
        {{ adapter.quote("OBS_TIME") }}

    from source
)
select * from renamed
  