import pandas as pd

# Read the CSV data into a pandas DataFrame
input_file = "EIA_Utility_Y2023.csv"  # Path to the input CSV file
output_file = "dbt_project/seeds/EIA_Utility_Y2023.csv"  # Path for the output file

# Define the column names if not included in the file
columns = [
    "Utility_ID", "Utility_Name", "Street_Address", "City", "State", "Zip",
    "Owner_of_Plants", "Operator_of_Plants", "Asset_Manager_of_Plants",
    "Other_Relationships", "Entity_Type"
]

# Load the CSV file into a DataFrame
df = pd.read_csv(input_file, names=columns, skiprows=1)

# Format: Strip whitespace, handle missing values, and normalize text case
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df['Zip'] = df['Zip'].astype(str)  # Ensure Zip is treated as a string
df.fillna('', inplace=True)  # Replace NaNs with empty strings

# Normalize column names to align with Snowflake standards
df.columns = [col.upper() for col in df.columns]

# Save the formatted data back to a new CSV file
df.to_csv(output_file, index=False)

print(f"Formatted data saved to {output_file}")
