import csv

# Define the file paths
input_file_path = "ghcnd-stations.txt"
output_file_path = "noaa_stations.csv"

# Open and parse the file
stations = []
with open(input_file_path, "r") as file:
    for line in file:
        station = {
            "ID": line[0:11].strip(),           # Columns 1-11
            "LATITUDE": float(line[12:20].strip()),  # Columns 13-20
            "LONGITUDE": float(line[21:30].strip()), # Columns 22-30
            "ELEVATION": float(line[31:37].strip()), # Columns 32-37
            "STATE": line[38:40].strip(),       # Columns 39-40
            "NAME": line[41:71].strip(),        # Columns 42-71
            "GSN_FLAG": line[72:75].strip(),    # Columns 73-75
            "HCN/CRN_FLAG": line[76:79].strip(),# Columns 77-79
            "WMO_ID": line[80:85].strip()       # Columns 81-85
        }
        stations.append(station)

# Write to a CSV file
with open(output_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=stations[0].keys())
    writer.writeheader()  # Write the header row
    writer.writerows(stations)  # Write the station data

print(f"Data saved to {output_file_path}")