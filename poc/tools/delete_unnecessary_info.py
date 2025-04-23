import json
import pandas as pd

# Load HR data
hr_data = pd.read_csv("data/hr_data.csv")
valid_cities = set(hr_data["City"].dropna().unique())

# Load and filter city GeoJSON based on 'id' field
with open("geojson/communes.indexed.geojson", encoding="utf-8") as f:
    city_geojson = json.load(f)

filtered_features = [f for f in city_geojson["features"] if f["id"] in valid_cities]

filtered_city_geojson = {**city_geojson, "features": filtered_features}

# Save filtered GeoJSON
with open("geojson/communes.filtered.geojson", "w", encoding="utf-8") as f:
    json.dump(filtered_city_geojson, f, ensure_ascii=False, indent=2)

print(f"Filtered GeoJSON saved with {len(filtered_features)} features.")
