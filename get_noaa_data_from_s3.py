import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, DateType, DoubleType

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
stage = "@my_s3_stage/"
file = "2024.csv"

stage_path = stage + file

print(stage_path)

schema = StructType([
    StructField("ID", StringType()),
    StructField("DATE", StringType()),
    StructField("ELEMENT", StringType()),
    StructField("DATA_VALUE", DoubleType()),
    StructField("M_FLAG", StringType()),
    StructField("Q_FLAG", StringType()),
    StructField("S_FLAG", StringType()),
    StructField("OBS_TIME", StringType())
])


# Read csv file from the s3 stage
df = session.read.schema(schema).options({"SKIP_HEADER": 1}).csv(stage_path)

# Write the data to the Snowflake table
df.write.mode("overwrite").save_as_table("raw_noaa_data")

# Show the data
df = session.table("raw_noaa_data")
df.show(10)

# Drop the table after testing
# session.sql("DROP TABLE IF EXISTS raw_noaa_data").collect()