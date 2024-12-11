import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, DateType, DoubleType
from snowflake.snowpark.functions import when_matched, when_not_matched
from include.eia_data_functions import create_snowflake_session


def create_noaa_table_in_snowflake(session):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS raw_noaa_data (
        ID STRING,
        DATE STRING,
        ELEMENT STRING,
        DATA_VALUE DOUBLE,
        M_FLAG STRING,
        Q_FLAG STRING,
        S_FLAG STRING,
        OBS_TIME STRING
    )
    """
    session.sql(create_table_sql).collect()


def merge_noaa_data_to_snowflake(ds):
    # Initialize Snowpark session
    session = create_snowflake_session()
    create_noaa_table_in_snowflake(session)
    
    # Stage for the public S3 bucket
    stage = "@my_s3_stage/"
    year = ds[:4]
    file = year + ".csv"

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

    target_table = session.table("raw_noaa_data")

    # Step 4: Perform the merge operation
    merge_result = target_table.merge(
        df,
        (target_table["ID"] == df["ID"]) &
        (target_table["DATE"] == df["DATE"]) &
        (target_table["ELEMENT"] == df["ELEMENT"]),
        [when_matched().update(
        {
            "DATA_VALUE": df["DATA_VALUE"],
            "M_FLAG": df["M_FLAG"],
            "Q_FLAG": df["Q_FLAG"],
            "S_FLAG": df["S_FLAG"],
            "OBS_TIME": df["OBS_TIME"]
        }),
        when_not_matched().insert(
        {
            "ID": df["ID"],
            "DATE": df["DATE"],
            "ELEMENT": df["ELEMENT"],
            "DATA_VALUE": df["DATA_VALUE"],
            "M_FLAG": df["M_FLAG"],
            "Q_FLAG": df["Q_FLAG"],
            "S_FLAG": df["S_FLAG"],
            "OBS_TIME": df["OBS_TIME"]
        })]
    )
    return merge_result
    
    # Write the data to the Snowflake table
    # df.write.mode("overwrite").save_as_table("raw_noaa_data")

# Show the data
# df = session.table("raw_noaa_data")
# df.show(10)