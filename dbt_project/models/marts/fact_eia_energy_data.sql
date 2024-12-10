WITH eia_energy_data AS (
  SELECT
    PERIOD,
    RESPONDENT,
    FUELTYPE,
    TYPE_NAME,
    VALUE
  FROM {{ ref('base_bootcamp_eia_fuel_type_data') }} AS base_bootcamp_eia_fuel_type_data
)
SELECT
  *
FROM eia_energy_data