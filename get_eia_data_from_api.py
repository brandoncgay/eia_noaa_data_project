import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, DoubleType

# Step 1: Configure Snowflake connection
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

session = Session.builder.configs(connection_parameters).create()

# Step 2: Fetch data from the EIA API
api_key = os.getenv("EIA_API_KEY")
url = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"
params = {
    "api_key": api_key,
    "frequency": "hourly",
    "start": "2023-01-01",
    "end": "2023-01-02",
    "data[]": "value"
}

response = requests.get(url, params=params)

data = response.json()["response"]["data"]
print(len(data))

# Step 3: Define Snowflake table schema
schema = StructType([
    StructField("period", StringType()),
    StructField("respondent", StringType()),
    StructField("respondent-name", StringType()),
    StructField("fueltype", StringType()),
    StructField("type-name", StringType()),
    StructField("value", DoubleType()),
    StructField("value-units", StringType())
])

# Step 4: Create a Snowpark DataFrame
rows = [(item["period"],
         item["respondent"], 
         item["respondent-name"], 
         item["fueltype"],
         item["type-name"],
         item["value"],
         item["value-units"]) for item in data]
df = session.create_dataframe(rows, schema=schema)

# Step 5: Write data to Snowflake table
df.write.mode("overwrite").save_as_table("eia_fuel_type_data")

# Step 6: Verify the data in Snowflake
df_in_snowflake = session.table("eia_fuel_type_data")
df_in_snowflake.show(10)
