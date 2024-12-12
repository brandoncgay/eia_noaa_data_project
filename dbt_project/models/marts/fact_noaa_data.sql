WITH noaa_data AS (
  SELECT
    d.date,
    d.id,
    d.element,
    d.data_value,
    s.latitude,
    s.longitude,
    s.state
  FROM {{ ref('base_bootcamp_raw_noaa_data') }} AS d
  JOIN {{ ref('noaa_stations') }} AS s
    ON d.id = s.id
  WHERE
    d.element IN ('TMIN', 'TMAX', 'PRCP', 'SNOW', 'SNWD', 'TSUN', 'WDMV')
    AND NOT s.state IS NULL
)
SELECT
  *
FROM noaa_data