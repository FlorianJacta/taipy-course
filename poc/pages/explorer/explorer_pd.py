import pandas as pd
import plotly.express as px
from taipy.gui import State, notify
import taipy.gui.builder as tgb
import json
import time

# =====================
# Load Data
# =====================
hr_data = pd.read_csv("data/hr_data.csv")

# Filters
sectors = ["Tout"] + sorted(hr_data["Secteur"].dropna().unique().tolist())
jobs = ["Tout"] + sorted(hr_data["Métier"].dropna().unique().tolist())
years = ["Tout"] + sorted([int(y) for y in hr_data["Année"].dropna().unique()])
regions = ["Tout"] + sorted(hr_data["Région"].dropna().unique().tolist())
departments = ["Tout"] + sorted(hr_data["Département"].dropna().unique().tolist())
levels = ["Région", "Département", "Ville"]

selected_sector = "Tout"
selected_job = "Tout"
selected_year = "Tout"
selected_level = "Région"
region_selected = "Tout"
department_selected = "Tout"

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
    "Région": (region_geojson, "id"),
    "Département": (department_geojson, "id"),
    "Ville": (city_geojson, "id"),
}


def filter_data(state):
    data = hr_data.copy()
    mask = data["Recrutement"] > 0
    if state.selected_sector != "Tout":
        mask &= data["Secteur"] == state.selected_sector
    if state.selected_job != "Tout":
        mask &= data["Métier"] == state.selected_job
    if state.selected_year != "Tout":
        mask &= data["Année"] == int(state.selected_year)
    if state.region_selected != "Tout":
        mask &= data["Région"] == state.region_selected
    if state.department_selected != "Tout":
        mask &= data["Département"] == state.department_selected

    data = data[mask]
    state.filtered_data = data


# =====================
# Map Generator
# =====================
def generate_hr_map(data, level, center, zoom):
    grouped = data
    geojson, feature_key = geojson_map[level]
    if not isinstance(center, dict):
        center = center._dict
    fig = px.choropleth_map(
        grouped,
        geojson=geojson,
        locations=level,
        featureidkey=feature_key,
        color="Recrutement",
        color_continuous_scale="Viridis",
        zoom=zoom,
        center=center,
        opacity=0.5,
        height=600,
        hover_data=["Recrutement"],
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_style="open-street-map"
    )
    return fig


def generate_charts(state):
    state.chart_data = (
        state.filtered_data.groupby(state.selected_level)["Recrutement"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    map_fig = generate_hr_map(
        state.chart_data, state.selected_level, state.center, state.zoom
    )
    if state.selected_level == "Région":
        state.map_fig_regions = map_fig
    if state.selected_level == "Département":
        state.map_fig_departments = map_fig
    if state.selected_level == "Ville":
        state.map_fig_communes = map_fig


def change_dynamic_lov(state):
    jobs = state.filtered_data["Métier"].unique().tolist()
    if len(jobs) > 1:
        state.jobs = ["Tout"] + jobs

    departements = state.filtered_data["Département"].unique().tolist()
    if len(departements) > 1:
        state.departments = ["Tout"] + departements


# =====================
# Apply Filters
# =====================
def apply_filters(state: State):
    with state:
        filter_data(state)

        if not state.filtered_data.empty:
            generate_charts(state)
            change_dynamic_lov(state)
        else:
            notify(state, "error", "No data available for the selected filters.")
            state.chart_data = pd.DataFrame()
            state.map_fig_regions = None
            state.map_fig_departments = None
            state.map_fig_communes = None


# =====================
# Map Click Handler
# =====================
def on_change(state: State, var_name, var_value):
    with state:
        if var_name == "selected_regions" and isinstance(var_value, list) and var_value:
            selected = var_value[0]
            if state.selected_level == "Région":
                region = state.map_fig_regions.data[0].locations[selected][0]
                state.region_selected = region
                state.selected_level = "Département"
                state.center = region_centers.get(region, {"lat": 46.5, "lon": 2.5})
                state.zoom = 6
            elif state.selected_level == "Département":
                department = state.map_fig_departments.data[0].locations[selected][0]
                state.department_selected = department
                state.selected_level = "Ville"
                state.zoom = 8
            apply_filters(state)


# =====================
# Initial Data
# =====================
filtered_data = hr_data.copy()
chart_data = (
    filtered_data.groupby(selected_level)["Recrutement"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

map_fig_regions = generate_hr_map(filtered_data, "Région", center, zoom)
map_fig_departments = generate_hr_map(filtered_data, "Département", center, zoom)
map_fig_communes = generate_hr_map(filtered_data, "Ville", center, zoom)

# =====================
# GUI Layout
# =====================
with tgb.Page() as explorer_page:
    tgb.text("## Carte des **besoins** et formations", mode="md")
    tgb.html("hr")
    with tgb.layout("1 3"):
        with tgb.part():
            tgb.metric(
                title="Recrutement logement 2025-2035",
                value=lambda filtered_data: filtered_data["Recrutement"].sum(),
                type="none",
                class_name="metric",
            )
            tgb.metric(
                title="Recrutement tertiaire 2025-2035",
                value=lambda filtered_data: filtered_data["Recrutement"].sum(),
                type="none",
                class_name="metric",
            )
            tgb.metric(
                title="Recrutement aménagements<br> urbains 2025-2035",
                value=lambda filtered_data: filtered_data["Recrutement"].sum(),
                type="none",
                class_name="metric",
            )
            tgb.metric(
                title="Nombre formées 2025-2035",
                value=lambda filtered_data: filtered_data["Recrutement"].sum(),
                type="none",
                class_name="metric",
            )
        with tgb.part():
            with tgb.part(class_name="card"):
                tgb.text("Paramètrage", class_name="h4")
                with tgb.layout(columns="1 1 1 1 1"):
                    tgb.selector(
                        label="Secteur",
                        value="{selected_sector}",
                        lov=sectors,
                        dropdown=True,
                        on_change=apply_filters,
                    )
                    tgb.selector(
                        label="Métier",
                        value="{selected_job}",
                        lov="{jobs}",
                        dropdown=True,
                        on_change=apply_filters,
                    )
                    tgb.selector(
                        label="Année",
                        value="{selected_year}",
                        lov=years,
                        dropdown=True,
                        on_change=apply_filters,
                    )

                    tgb.selector(
                        label="Région",
                        value="{region_selected}",
                        lov="{regions}",
                        dropdown=True,
                        on_change=apply_filters,
                    )

                    tgb.selector(
                        label="Département",
                        value="{department_selected}",
                        lov="{departments}",
                        dropdown=True,
                        on_change=apply_filters,
                    )

            tgb.toggle(
                value="{selected_level}",
                lov=levels,
                dropdown=True,
                on_change=generate_charts,
            )

            tgb.chart(
                figure="{map_fig_regions}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "Région",
            )
            tgb.chart(
                figure="{map_fig_departments}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "Département",
            )
            tgb.chart(
                figure="{map_fig_communes}",
                selected="{selected_regions}",
                render=lambda selected_level: selected_level == "Ville",
            )

            tgb.chart(
                data="{chart_data}",
                x="{selected_level}",
                y="Recrutement",
                type="bar",
                rebuild=True,
            )
            tgb.table(data="{filtered_data}", page_size=10)
