import polars as pl
import plotly.express as px
from taipy.gui import State
import taipy.gui.builder as tgb
import json
import time

# =====================
# Load Data
# =====================
hr_data = pl.read_csv("data/hr_data.csv")

# Filters
sectors = ["All"] + sorted(
    hr_data.select("Sector").drop_nulls().unique().to_series().to_list()
)
jobs = ["All"] + sorted(
    hr_data.select("Job Title").drop_nulls().unique().to_series().to_list()
)
years = ["All"] + sorted(
    [int(y) for y in hr_data.select("Year").drop_nulls().unique().to_series().to_list()]
)
levels = ["Region", "Department", "City"]

selected_sector = "All"
selected_job = "All"
selected_year = "All"
selected_level = "Region"

region_selected = "All"
department_selected = "All"

selected_regions = []
selected_departments = []

zoom = 4.5
center = {"lat": 46.5, "lon": 2.5}

# =====================
# Load GeoJSONs
# =====================
with open("geojson/regions.indexed.geojson", encoding="utf-8") as f:
    region_geojson = json.load(f)
with open("geojson/departements.indexed.geojson", encoding="utf-8") as f:
    department_geojson = json.load(f)
with open("geojson/communes.filtered.geojson", encoding="utf-8") as f:
    city_geojson = json.load(f)
with open("geojson/regions_center.json", encoding="utf-8") as f:
    region_centers = json.load(f)

geojson_map = {
    "Region": (region_geojson, "id"),
    "Department": (department_geojson, "id"),
    "City": (city_geojson, "id"),
}


# =====================
# Map Generator
# =====================uv
def generate_hr_map(data: pl.DataFrame, level, center, zoom):
    grouped = data.group_by(level).agg(pl.col("Employees Needed").sum()).sort(level)
    geojson, feature_key = geojson_map[level]
    if not isinstance(center, dict):
        center = center._dict
    fig = px.choropleth_map(
        grouped,
        geojson=geojson,
        locations=level,
        featureidkey=feature_key,
        color="Employees Needed",
        color_continuous_scale="Viridis",
        zoom=zoom,
        center=center,
        opacity=0.5,
        height=600,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_style="open-street-map"
    )
    return fig


# =====================
# Apply Filters
# =====================
def apply_filters(state: State):
    start = time.time()
    with state:
        data = hr_data.clone()
        if state.selected_sector != "All":
            data = data.filter(pl.col("Sector") == state.selected_sector)
        if state.selected_job != "All":
            data = data.filter(pl.col("Job Title") == state.selected_job)
        if state.selected_year != "All":
            data = data.filter(pl.col("Year") == int(state.selected_year))
        if state.region_selected != "All":
            data = data.filter(pl.col("Region") == state.region_selected)
        if state.department_selected != "All":
            data = data.filter(pl.col("Department") == state.department_selected)

        state.filtered_data = data

        if data.height > 0:
            chart = data.group_by(state.selected_level).agg(
                pl.col("Employees Needed").sum()
            )
            chart = chart.sort("Employees Needed", descending=True)
            state.chart_data = chart

            if state.selected_level == "Region":
                state.map_fig_regions = generate_hr_map(
                    data, "Region", state.center, state.zoom
                )
            if state.selected_level == "Department":
                state.map_fig_departments = generate_hr_map(
                    data, "Department", state.center, state.zoom
                )
            if state.selected_level == "City":
                state.map_fig_communes = generate_hr_map(
                    data, "City", state.center, state.zoom
                )

        else:
            import pandas as pd

            state.chart_data = pd.DataFrame()
            state.map_fig_regions = None
            state.map_fig_departments = None
            state.map_fig_communes = None

    print(f"Filters applied in {time.time() - start:.2f} seconds")


# =====================
# Map Click Handler
# =====================
def on_change(state: State, var_name, var_value):
    with state:
        if var_name == "selected_regions" and isinstance(var_value, list) and var_value:
            selected = var_value[0]
            if state.selected_level == "Region":
                region = state.map_fig_regions.data[0].locations[selected][0]
                state.region_selected = region
                state.selected_level = "Department"
                state.center = region_centers.get(region, {"lat": 46.5, "lon": 2.5})
                state.zoom = 6
            elif state.selected_level == "Department":
                department = state.map_fig_departments.data[0].locations[selected][0]
                state.department_selected = department
                state.selected_level = "City"
                state.zoom = 8
            apply_filters(state)


# =====================
# Initial Data
# =====================
filtered_data = hr_data.clone()
chart_data = filtered_data

map_fig_regions = generate_hr_map(hr_data, "Region", center, zoom)
map_fig_departments = generate_hr_map(hr_data, "Department", center, zoom)
map_fig_communes = generate_hr_map(hr_data, "City", center, zoom)

# =====================
# GUI Layout
# =====================
with tgb.Page() as explorer_page:
    with tgb.layout("1 3"):
        with tgb.part():
            tgb.metric(
                label="Total Employees Needed",
                value=lambda filtered_data: filtered_data["Employees Needed"].sum(),
                type="none",
                class_name="metric",
            )
        with tgb.part():
            with tgb.part(class_name="card"):
                with tgb.layout(columns="1 1 1 1"):
                    tgb.selector(
                        label="Sector",
                        value="{selected_sector}",
                        lov=sectors,
                        dropdown=True,
                        on_change=apply_filters,
                    )
                    tgb.selector(
                        label="Job Title",
                        value="{selected_job}",
                        lov=jobs,
                        dropdown=True,
                        on_change=apply_filters,
                    )
                    tgb.selector(
                        label="Year",
                        value="{selected_year}",
                        lov=years,
                        dropdown=True,
                        on_change=apply_filters,
                    )
                    tgb.selector(
                        label="Level",
                        value="{selected_level}",
                        lov=levels,
                        dropdown=True,
                    )

                    tgb.selector(
                        label="Region",
                        value="{region_selected}",
                        lov=lambda hr_data: ["All"]
                        + sorted(
                            hr_data.select("Region")
                            .drop_nulls()
                            .unique()
                            .to_series()
                            .to_list()
                        ),
                        dropdown=True,
                        on_change=apply_filters,
                    )

                    tgb.selector(
                        label="Department",
                        value="{department_selected}",
                        lov=lambda filtered_data: ["All"]
                        + sorted(
                            filtered_data.select("Department")
                            .drop_nulls()
                            .unique()
                            .to_series()
                            .to_list()
                        ),
                        dropdown=True,
                        on_change=apply_filters,
                    )

            tgb.chart(
                figure="{map_fig_regions}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "Region",
            )
            tgb.chart(
                figure="{map_fig_departments}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "Department",
            )
            tgb.chart(
                figure="{map_fig_communes}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "City",
            )

            tgb.chart(
                data="{chart_data.to_pandas()}",
                x="{selected_level}",
                y="Employees Needed",
                type="bar",
            )
            tgb.table(data="{filtered_data.to_pandas()}", page_size=10)
