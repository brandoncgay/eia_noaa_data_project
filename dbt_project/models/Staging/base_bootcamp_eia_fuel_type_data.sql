{{ config(
    materialized='view'
) }}

with source as (
      select * from {{ source('bootcamp', 'eia_fuel_type_data') }}
),
renamed as (
    select
        {{ adapter.quote("PERIOD") }},
        {{ adapter.quote("RESPONDENT") }},
        {{ adapter.quote("RESPONDENT_NAME") }},
        {{ adapter.quote("FUELTYPE") }},
        {{ adapter.quote("TYPE_NAME") }},
        {{ adapter.quote("VALUE") }},
        {{ adapter.quote("VALUE_UNITS") }}

    from source
)
select * from renamed
  