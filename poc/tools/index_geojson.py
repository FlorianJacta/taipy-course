import geopandas as gpd
import json
import sys
import os

# Read command line arguments and check for potential errors
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input_geojson_file>")
    print("Generates a pre-indexed version of the GeoJSON data.")
    exit(1)
if not os.path.exists(sys.argv[1]):
    print(f"ERROR: Couldn't read input GeoJson file: {sys.argv[1]}")
    exit(1)
parts = os.path.splitext(sys.argv[1])
output_file = f"{parts[0]}.indexed{parts[1]}"
if os.path.exists(output_file):
    print(f"ERROR: Output file {output_file} already exists")
    exit(1)

gdf = gpd.read_file(sys.argv[1], encoding="utf-8")
geojson = json.loads(gdf.set_index("nom").to_json())

print(f"Generating {output_file}")
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(geojson, file, ensure_ascii=False)
