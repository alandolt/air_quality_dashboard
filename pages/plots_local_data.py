import dash
from dash import html, Input, Output, callback, dcc
import copy
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from air_quality_dashboard.data_parser import local_data
from geopy.geocoders import Nominatim


dash.register_page(__name__, path="/localdata", name="Plots Local data")
plotly.io.templates.default = "plotly_white"

ITEMS_PER_PAGE = 10  # set the number of elements per page

localdata = local_data.LocalData()

df = localdata.df

filtered_location = df.drop_duplicates(subset="Location").sort_values(by="Location")

geolocator = Nominatim(user_agent="my_geocoder")

geocoded_data = []

for location in filtered_location["Location"]:
    location_info = geolocator.geocode(location + ", Switzerland")
    if location_info:
        geocoded_data.append(
            {
                "Location": location,
                "Latitude": location_info.latitude,
                "Longitude": location_info.longitude,
            }
        )

geocoded_df = pd.DataFrame(geocoded_data)


df["date"] = df["timestamp"].dt.date
filter_date = df.drop_duplicates(subset="date").sort_values(by="date")


dropdown_style_date = {"width": "400px"}
dropdown_style_concentration = {"width": "200px"}

layout = html.Div(
    [
        html.H1("Local Data Statistics"),
        html.H2("See concentrations in function of the date in Switzerland"),
        html.Div(
            [
                html.H5("Date"),
                dcc.Dropdown(
                    id="date",
                    options=[
                        {"label": date.strftime("%Y-%m-%d"), "value": date}
                        for date in filter_date["timestamp"]
                    ],
                    value=filter_date["timestamp"].iloc[0],
                    style=dropdown_style_date,
                    clearable=False,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.H5("Concentration"),
                dcc.Dropdown(
                    id="concentration-selector",
                    options=[
                        {"label": "O3", "value": "O3"},
                        {"label": "NO2", "value": "NO2"},
                        {"label": "PM10", "value": "PM10"},
                    ],
                    value="O3",
                    style=dropdown_style_concentration,
                    clearable=False,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            dcc.Graph(id="switzerland"),
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
    ]
)


@callback(
    Output(component_id="switzerland", component_property="figure"),
    Input(component_id="date", component_property="value"),
    Input(component_id="concentration-selector", component_property="value"),
)
def switzerland_concentrations(date, concentration):
    dff = df.dropna(subset=[concentration], inplace=True)
    dff = df[df["timestamp"] == date]
    dff = dff.groupby(["Location"]).mean(numeric_only=True).reset_index()
    merged_df = pd.merge(dff, geocoded_df, on="Location")

    fig = px.scatter_mapbox(
        merged_df,
        lat="Latitude",
        lon="Longitude",
        mapbox_style="open-street-map",
        size=concentration,
        color=concentration,
        center={"lat": 46.8182, "lon": 8.2275},
        zoom=7,
        size_max=20,
    )

    fig.update_layout(
        width=1000,
        height=800,
        title=f"mean {concentration} concentration on a specific date in Switzerland",
    )

    return fig
