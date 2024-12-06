import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, FloatType

# Snowflake connection parameters
load_dotenv()
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

# Initialize Snowpark session
session = Session.builder.configs(connection_parameters).create()

# Stage for the public S3 bucket
stage = "@noaa_s3_stage/"
file = "ghcnd-stations.txt"

stage_path = stage + file

# Define schema for the fixed-width file
schema = StructType([
    StructField("Station_ID", StringType()),
    StructField("Latitude", FloatType()),
    StructField("Longitude", FloatType()),
    StructField("Elevation", FloatType()),
    StructField("State", StringType()),
    StructField("Location_Name", StringType())
])

# Define parsing function for fixed-width format
def parse_fixed_width_line(line):
    return {
        "Station_ID": line[0:11].strip(),
        "Latitude": float(line[12:21].strip()),
        "Longitude": float(line[22:31].strip()),
        "Elevation": float(line[32:40].strip()),
        "Location_Name": line[41:82].strip()
    }
    
# Load the raw text file into a Snowflake table
session.sql(f"""
    CREATE OR REPLACE TEMP TABLE raw_lines (line STRING)
""").collect()

session.sql(f"""
    COPY INTO raw_lines
    FROM {stage_path}
    FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = NONE SKIP_HEADER = 0 RECORD_DELIMITER = '\n' FIELD_DELIMITER = NONE);
""").collect()

# Parse fixed-width fields using SQL
parsed_df = session.sql("""
    SELECT
        TRIM(SUBSTR(line, 1, 11)) AS Station_ID,        -- First 11 characters
        TRY_CAST(TRIM(SUBSTR(line, 13, 7)) AS FLOAT) AS Latitude,  -- Next 9 characters
        TRY_CAST(TRIM(SUBSTR(line, 22, 8)) AS FLOAT) AS Longitude, -- Next 9 characters
        TRY_CAST(TRIM(SUBSTR(line, 32, 5)) AS FLOAT) AS Elevation, -- Next 8 characters
        TRIM(SUBSTR(line, 39, 2))  AS State,
        TRIM(SUBSTR(line, 42, 29)) AS Location_Name     -- Remaining characters
    FROM raw_lines
""")

# Write data to table
parsed_df.write.save_as_table("noaa_stations", mode="overwrite")
