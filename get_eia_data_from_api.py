import requests, os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, DoubleType
from snowflake.snowpark.functions import when_matched, when_not_matched

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
limit = 5000
offset = 0
all_data = []
start_date = "2023-01-01"
end_date = "2023-01-02"

while True: 
    params = {
        "api_key": api_key,
        "frequency": "hourly",
        "start": start_date,
        "end": end_date,
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
         item["value-units"]) for item in all_data]
df = session.create_dataframe(rows, schema=schema)

df.show(10)

target_table = session.table("eia_fuel_type_data")

# Step 4: Perform the merge operation
merge_result = target_table.merge(
    df,
    (target_table["period"] == df["period"]) &
    (target_table["respondent"] == df["respondent"]) &
    (target_table["fueltype"] == df["fueltype"]),
    [when_matched().update(
    {
        "respondent-name": df["respondent-name"],
        "type-name": df["type-name"],
        "value": df["value"],
        "value-units": df["value-units"]
    }),
    when_not_matched().insert(
    {
        "period": df["period"],
        "respondent": df["respondent"],
        "respondent-name": df["respondent-name"],
        "fueltype": df["fueltype"],
        "type-name": df["type-name"],
        "value": df["value"],
        "value-units": df["value-units"]
    })]
)


print(merge_result)

# Step 5: Write data to Snowflake table
# df.write.mode("overwrite").save_as_table("eia_fuel_type_data")

# Step 6: Verify the data in Snowflake
# df_in_snowflake = session.table("eia_fuel_type_data")
# df_in_snowflake.show(10)
