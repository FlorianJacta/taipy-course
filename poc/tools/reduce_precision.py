import json
import os
import sys

# Read command line arguments and check for potential errors
if len(sys.argv) != 4:
    print(
        f"Usage: {sys.argv[0]} <input_geojson_file> <output_geojson_file> <precision>"
    )
    exit(1)
if not os.path.exists(sys.argv[1]):
    print(f"ERROR: Couldn't read input GeoJson file: {sys.argv[1]}")
    exit(1)
if os.path.exists(sys.argv[2]):
    print(f"ERROR: Output file {sys.argv[2]} already exists")
    exit(1)
precision = 0
if not sys.argv[3].isdigit():
    print(f"ERROR: Precision must be an integer value (found '{sys.argv[3]}')")
    exit(1)
precision = int(sys.argv[3])
if precision < 1 or precision > 15:
    print(f"ERROR: Precision must be positive and less than 15 (found '{precision}')")
    exit(1)

# Load the GeoJSON file
input_file_size = os.stat(sys.argv[1]).st_size // 1024 // 1024
print(f"Input file size: {input_file_size} Mb")
with open(sys.argv[1], "r") as file:
    data = json.load(file)


# Round all coordinate values and remove duplicates
def reduce_list(coords):
    """Recursively rounds coordinates to the specified precision."""
    if isinstance(coords[0], list):
        return [reduce_list(coord) for coord in coords]
    last_coord = None
    new_coord_list = []
    for coord in coords:
        new_coord = round(coord, precision)
        if new_coord.is_integer():
            new_coord = int(new_coord)
        if new_coord != last_coord:
            last_coord = new_coord
            new_coord_list.append(new_coord)
    return new_coord_list


for feature in data["features"]:
    geometry = feature["geometry"]
    if geometry["type"] in ["Polygon", "MultiPolygon"]:
        geometry["coordinates"] = reduce_list(geometry["coordinates"])

# Save the modified GeoJSON
with open(sys.argv[2], "w") as file:
    json.dump(data, file)
output_file_size = os.stat(sys.argv[2]).st_size // 1024 // 1024
print(f"Output file size: {output_file_size} Mb")
