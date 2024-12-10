WITH plant_distance_to_nearest_station AS (
  SELECT
    PLANT_CODE,
    MIN(DISTANCE_M) AS DISTANCE_M
  FROM {{ ref('stations_with_nearest_plant') }} AS stations_with_nearest_plant
  GROUP BY
    1
), plants_with_nearest_station AS (
  SELECT
    a.PLANT_CODE,
    b.ID AS STATION_ID,
    a.DISTANCE_M
  FROM plant_distance_to_nearest_station AS a
  JOIN {{ ref('stations_with_nearest_plant') }} AS b
    ON a.plant_code = b.plant_code AND a.distance_m = b.distance_m
)
SELECT
  *
FROM plants_with_nearest_station