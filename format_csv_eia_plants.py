import pandas as pd
import os

# Input and output file paths
input_file = "EIA_Plant_Y2023.csv"  # Path to the input CSV file
output_file = "dbt_project/seeds/EIA_Plant_Y2023.csv"  # Path for the output file

def clean_and_format_csv(input_path, output_path):
    """
    Cleans and formats the CSV data for Snowflake ingestion.
    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned CSV file.
    """
    try:
        # Read the CSV file with `low_memory=False` to handle large files and mixed types
        df = pd.read_csv(input_path, low_memory=False)

        # Clean column names: replace spaces with underscores, remove special characters, and make them lowercase
        df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_').str.lower()

        # Handle missing values: Replace NaNs with appropriate defaults
        for col in df.columns:
            # Handle string columns (e.g., fill NaNs with empty strings)
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('')  # Fill missing strings with empty string
                df[col] = df[col].str.strip()  # Clean leading/trailing whitespaces
            else:
                # For numeric columns, replace NaNs with 0
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)  # Fill NaNs with 0 for numeric columns

        # Ensure all latitude and longitude columns are numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors="coerce")
        df['longitude'] = pd.to_numeric(df['longitude'], errors="coerce")

        # Optional: Format 'zip' to be consistent (if necessary)
        df['zip'] = df['zip'].apply(lambda x: str(x).zfill(5))  # Ensure all ZIP codes are 5 digits

        # Save the cleaned dataframe to a new CSV file
        df.to_csv(output_path, index=False)

        print(f"Data successfully formatted and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
clean_and_format_csv(input_file, output_file)
