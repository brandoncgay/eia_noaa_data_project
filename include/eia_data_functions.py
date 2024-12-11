import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, DoubleType
from snowflake.snowpark.functions import when_matched, when_not_matched
from airflow.macros import ds_add, ds_format

# Step 1: Configure Snowflake connection
def create_snowflake_session():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA")
    }

    session = Session.builder.configs(connection_parameters).create()
    return session

def create_eia_table_in_snowflake(session):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS eia_fuel_type_data (
        period STRING,
        respondent STRING,
        respondent_name STRING,
        fueltype STRING,
        type_name STRING,
        timezone STRING,
        timezone_description STRING,
        value DOUBLE,
        value_units STRING
    )
    """
    session.sql(create_table_sql).collect()

# Step 2: Fetch data from the EIA API
def get_eia_data_from_api(ds):
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    api_key = os.getenv("EIA_API_KEY")
    url = "https://api.eia.gov/v2/electricity/rto/daily-fuel-type-data/data/"
    limit = 5000
    offset = 0
    all_data = []
    start_date = ds_add(ds, -1)
    end_date = start_date
    
    print("start date: " + start_date)
    print("end date: " + end_date)

    while True: 
        params = {
            "api_key": api_key,
            "frequency": "daily",
            "start": start_date,
            "end": end_date,
            "facets[timezone][]": "Pacific",
            "data[]": "value",
            "offset": offset,
            "length": limit
        }

        response = requests.get(url, params=params)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'data' in data['response']:
                data_items = data['response']['data']
                all_data.extend(data_items)
                
                # If the number of results is less than the limit, we are done
                if len(data_items) < limit:
                    break
                else:
                    # Otherwise, increase the offset to get the next page of results
                    offset += limit
            else:
                print("No data found in response.")
                break
        else:
            print(f"Error: {response.status_code}")
            break
    print(len(all_data))
    return all_data

# Step 3: Define Snowflake table schema
def merge_eia_data_to_snowflake(data):
    session = create_snowflake_session()
    create_eia_table_in_snowflake(session)
    
    schema = StructType([
        StructField("period", StringType()),
        StructField("respondent", StringType()),
        StructField("respondent_name", StringType()),
        StructField("fueltype", StringType()),
        StructField("type_name", StringType()),
        StructField("timezone", StringType()),
        StructField("timezone_description", StringType()),
        StructField("value", DoubleType()),
        StructField("value_units", StringType())
    ])

    # Step 4: Create a Snowpark DataFrame
    rows = [(item["period"],
            item["respondent"], 
            item["respondent-name"], 
            item["fueltype"],
            item["type-name"],
            item["timezone"],
            item["timezone-description"],
            item["value"],
            item["value-units"]) for item in data]
    df = session.create_dataframe(rows, schema=schema)
    
    df.show(10)

    target_table = session.table("eia_fuel_type_data")

    # Step 4: Perform the merge operation
    merge_result = target_table.merge(
        df,
        (target_table["period"] == df["period"]) &
        (target_table["respondent"] == df["respondent"]) &
        (target_table["fueltype"] == df["fueltype"]) &
        (target_table["timezone"] == df["timezone"]),
        [when_matched().update(
        {
            "respondent_name": df["respondent_name"],
            "type_name": df["type_name"],
            "timezone_description": df["timezone_description"],
            "value": df["value"],
            "value_units": df["value_units"]
        }),
        when_not_matched().insert(
        {
            "period": df["period"],
            "respondent": df["respondent"],
            "respondent_name": df["respondent_name"],
            "fueltype": df["fueltype"],
            "type_name": df["type_name"],
            "timezone": df["timezone"],
            "timezone_description": df["timezone_description"],
            "value": df["value"],
            "value_units": df["value_units"]
        })]
    )
    return merge_result
