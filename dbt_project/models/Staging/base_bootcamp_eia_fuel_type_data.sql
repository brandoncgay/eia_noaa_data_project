WITH source AS (
  SELECT
    *
  FROM {{ source('bootcamp', 'eia_fuel_type_data') }} AS eia_fuel_type_data
), renamed AS (
  SELECT
    "PERIOD",
    "RESPONDENT",
    "RESPONDENT_NAME",
    "FUELTYPE",
    "TYPE_NAME",
    "VALUE",
    "VALUE_UNITS"
  FROM source
)
SELECT
  *
FROM renamed