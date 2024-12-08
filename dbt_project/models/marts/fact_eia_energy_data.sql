{{ config(
    materialized='table'
) }}

with eia_energy_data as (
    select
        PERIOD,
        RESPONDENT,
        FUELTYPE,
        TYPE_NAME,
        VALUE
    from {{ ref('base_bootcamp_eia_fuel_type_data')}}
)

select * from eia_energy_data