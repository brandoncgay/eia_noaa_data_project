WITH plant_gen_joined AS (
  SELECT
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
  FROM {{ ref('tmp_plant_data') }} AS p
  JOIN {{ ref('tmp_generator_data') }} AS g
    ON g.PLANT_CODE = p.PLANT_CODE
  JOIN {{ ref('tmp_plants_with_nearest_station') }} AS s
    ON p.PLANT_CODE = s.PLANT_CODE
)
SELECT
  *
FROM plant_gen_joined