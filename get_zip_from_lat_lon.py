import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the CSV files into pandas DataFrames
stations_df = pd.read_csv('dbt_project/seeds/noaa_stations.csv')  # Replace with the actual path to your stations CSV file
zip_codes_df = pd.read_csv('dbt_project/seeds/USZipsWithLatLon_20231227.csv')  # Replace with the actual path to your zip codes CSV file

# Function to convert DataFrame to GeoDataFrame
def create_geodataframe(df, lat_col, lon_col, crs="EPSG:4326"):
    """Create a GeoDataFrame from lat/lon columns"""
    # Create a list of Points
    points = [Point(lon, lat) for lat, lon in zip(df[lat_col], df[lon_col])]
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=points, crs=crs)
    return gdf

# Convert stations and zip codes to GeoDataFrames
stations_gdf = create_geodataframe(stations_df, "LATITUDE", "LONGITUDE")
zip_codes_gdf = create_geodataframe(zip_codes_df, "latitude", "longitude")

# Reproject to a projected CRS (e.g., EPSG:3857 for Web Mercator)
stations_gdf = stations_gdf.to_crs(epsg=3857)
zip_codes_gdf = zip_codes_gdf.to_crs(epsg=3857)

# Perform spatial join to find the nearest zip code for each station
nearest_zip = gpd.sjoin_nearest(stations_gdf, zip_codes_gdf, how="left", distance_col="distance_m")

# Output the results
nearest_zip[['ID', 'postal_code', 'distance_m']].to_csv('stations_with_nearest_zip.csv', index=False)

print("The nearest zip codes for each station have been saved to 'stations_with_nearest_zip.csv'.")