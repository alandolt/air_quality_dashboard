# Statistics page layout, for histogram graph.
# For the next task also graph would be nice.  Also add a third page with local_data

import dash
from dash import html, Input, Output, callback, dcc
import copy
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from air_quality_dashboard.data_parser import who_data

# register page for navigation selection
dash.register_page(__name__, path="/whodata", name="Plots WHO data")
plotly.io.templates.default = "plotly_white"


ITEMS_PER_PAGE = 10  # set the number of elements per page
# init instance whodata class, to have access to stored data
whodata = who_data.WHOData()

# Filter the countries and years for the dropdown menu
filter_years = whodata.df.drop_duplicates(subset="year").sort_values(by="year")
filtered_countries = whodata.df.drop_duplicates(subset="country_name").sort_values(
    by="country_name"
)

# Filter first string of type of stations for easier manipulation
dff = whodata.df

dff["type_of_stations"] = dff["type_of_stations"].str.replace(",", " ")
dff["type_of_stations"] = dff["type_of_stations"].str.split().str[0]
filtered_stations = dff.drop_duplicates(subset="type_of_stations").sort_values(
    by="type_of_stations"
)

dropdown_style_year = {"width": "200px"}
dropdown_style_country = {"width": "600px"}
dropdown_style_station = {"width": "400px"}
dropdown_style_concentration = {"width": "200px"}

layout = html.Div(
    [
        html.H1("WHOdata Statistics"),
        # Dropdown menus to chose different countries and their corresponding max_value in a certain timespan
        # Dropdown menus for years
        html.H2(
            "See max values in function of the country, timespan and concentration (Task2)"
        ),
        html.Div(
            [
                html.H5("Year 1"),
                dcc.Dropdown(
                    id="year-1",
                    options=[
                        {"label": row_year["year_int"], "value": row_year["year"]}
                        for index, row_year in filter_years.iterrows()
                    ],
                    value=filter_years["year"].iloc[0],
                    style=dropdown_style_year,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.H5("Year 2"),
                dcc.Dropdown(
                    id="year-2",
                    options=[
                        {"label": row_year["year_int"], "value": row_year["year"]}
                        for index, row_year in filter_years.iterrows()
                    ],
                    value=filter_years["year"].iloc[1],
                    style=dropdown_style_year,
                ),
            ],
            style={"display": "inline-block"},
        ),
        # Dropdown menu for countrys
        html.Div(
            [
                html.H5("Country"),
                dcc.Dropdown(
                    id="countries",
                    options=[
                        {
                            "label": row_country["country_name"],
                            "value": row_country["country_name"],
                        }
                        for index, row_country in filtered_countries.iterrows()
                    ],
                    value=["Switzerland", "Spain", "Norway"],
                    style=dropdown_style_country,
                    multi=True,
                ),
            ],
            style={"display": "inline-block"},
        ),
        # Put a Bar Plot for the max values
        dcc.Graph(id="bar-max"),
        # Begin layout for the globe representation
        html.H2("See a representation of different concentrations in the world."),
        # Put maybe a small explanation about the simulation
        html.Div(
            [
                html.H5("Concentration"),
                dcc.Dropdown(
                    id="concentration-selector",
                    options=[
                        {"label": "PM10", "value": "pm10_concentration"},
                        {"label": "PM25", "value": "pm25_concentration"},
                        {"label": "NO2", "value": "no2_concentration"},
                    ],
                    value="pm10_concentration",
                    style=dropdown_style_concentration,
                ),
            ],
            style={"display": "inline-block"},
        ),
        # Dropdown menu for type of stations
        html.Div(
            [
                html.H5("Type of station"),
                dcc.Dropdown(
                    id="station",
                    options=[
                        {
                            "label": row_stations["type_of_stations"],
                            "value": row_stations["type_of_stations"],
                        }
                        for index, row_stations in filtered_stations.iterrows()
                    ],
                    value=None,
                    style=dropdown_style_station,
                ),
            ],
            style={"display": "inline-block"},
        ),
        # Dropdown menu for the country to zoom in.
        html.Div(
            [
                html.H5("Country to center"),
                dcc.Dropdown(
                    id="country",
                    options=[
                        {
                            "label": row_country["country_name"],
                            "value": row_country["country_name"],
                        }
                        for index, row_country in filtered_countries.iterrows()
                    ],
                    value=None,
                    style=dropdown_style_country,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            dcc.Graph(id="globe"),
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
        # Begin of Layout for Boxplot and points over year
        html.H2(
            "See mean concentration of all countries over the years (just for fun)"
        ),
        # Selection with dropdown menu for different concentrations for graph plotting
        dcc.Dropdown(
            id="graph-selector",
            options=[
                {"label": "PM10", "value": "pm10_concentration"},
                {"label": "PM25", "value": "pm25_concentration"},
                {"label": "NO2", "value": "no2_concentration"},
            ],
            value="pm10_concentration",
        ),
        dcc.Graph(id="graph"),
    ]
)


@callback(
    Output(component_id="bar-max", component_property="figure"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="year-1", component_property="value"),
    Input(component_id="year-2", component_property="value"),
)
def update_bar_max(countries, year_1, year_2):
    """
    Barplot which presents the max values in function of the country
    """
    country_list = countries
    if isinstance(
        countries, str
    ):  # if only one country is selected, dash returns a string,
        #  which can't be used for the compairson, hence convert it to a list.
        country_list = list(countries)
    # filter the dataframe for the year + country
    df = whodata.df[
        (whodata.df["year"] >= year_1)
        & (whodata.df["year"] <= year_2)
        & (whodata.df["country_name"].isin(country_list))
    ]

    # test if for the chosen combination of polluant, and timespan one of the polluant
    # data is not available, if yes, print no matching data found.
    # algorithme however could be improved, here it serves as a proof of concept.
    if (
        df[["pm10_concentration", "pm25_concentration", "no2_concentration"]]
        .isnull()
        .all()
        .any()
    ):
        return {
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [
                    {
                        "text": "No matching data found",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {"size": 28},
                    }
                ],
            }
        }

    # create a new dataframe with only max values
    df_max = (
        df.groupby("country_name")[
            ["pm10_concentration", "pm25_concentration", "no2_concentration"]
        ]
        .max()
        .reset_index()
    )
    # convert from wide to long datafromat
    df_max = pd.melt(
        df_max,
        id_vars=["country_name"],
        value_vars=["pm10_concentration", "pm25_concentration", "no2_concentration"],
    )
    # add when the observation of the max value had been made
    df_max.loc[df_max["variable"] == "pm10_concentration", "year"] = df.loc[
        df.groupby("country_name")["pm10_concentration"].idxmax(), "year_int"
    ].values
    df_max.loc[df_max["variable"] == "pm25_concentration", "year"] = df.loc[
        df.groupby("country_name")["pm25_concentration"].idxmax(), "year_int"
    ].values
    df_max.loc[df_max["variable"] == "no2_concentration", "year"] = df.loc[
        df.groupby("country_name")["no2_concentration"].idxmax(), "year_int"
    ].values
    # for hoover overlay, we need a customdata list with the year + value
    customdata = np.stack((df_max["value"], df_max["year"]), axis=-1)
    df_max = df_max.replace(
        to_replace={
            "pm10_concentration": "PM10",
            "pm25_concentration": "PM25",
            "no2_concentration": "NO2",
        }
    )
    # convert float year to int, if not possible, as it does not exist (Nan), print NA
    try:
        year_min_str = str(int(df["year_int"].min()))
        year_max_str = str(int(df["year_int"].max()))
    except ValueError:
        year_min_str = "NA"
        year_max_str = "NA"
    # add a barplot (using histogram element from plotly express, as it enables us to use more
    # finetuning parameters)
    fig = px.histogram(
        data_frame=df_max,
        x="country_name",
        y="value",
        color="variable",
        barmode="group",
        title=f"Air quality data from {year_min_str} to {year_max_str}",
        color_discrete_sequence=px.colors.qualitative.D3,
    )
    # change axe labeling and legend
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Max concentration [ug/m<sup>3</sup>]",
        legend_title_text="Polluant",
    )
    # add hoover traces
    fig.update_traces(
        customdata=customdata,
        hovertemplate="<b>Concentration:</b> %{y} ug/m<sup>3</sup><br> <b>Year of max. data:</b> %{customdata[1]} <extra></extra>",
    )
    return fig


# Dynamic callback to filter out if there is a station avialbe for a country or not
# https://dash-example-index.herokuapp.com/dynamic-callback


@callback(
    Output("station", "options"),
    Input("country", "value"),
    Input("concentration-selector", "value"),
)

# function to filter out the stations in function of the countries


def chained_callback_station(country, concentration):
    dff = copy.deepcopy(whodata.df)
    if country is not None:
        dff = dff[dff["country_name"] == country]
        dff.dropna(subset=["type_of_stations"], inplace=True)
        # dff.dropna(subset=[concentration], inplace=True)
    # Convert all station types to strings
    station_types = dff["type_of_stations"].astype(str).unique()
    return [{"label": station, "value": station} for station in sorted(station_types)]


@callback(
    Output("country", "options"),
    Input("station", "value"),
    Input("concentration-selector", "value"),
)

# function to filter out the countries in function of the stations


def chained_callback_country(station, concentration):
    dff = copy.deepcopy(whodata.df)
    if station is not None:
        dff = dff[dff["type_of_stations"] == station]
        dff.dropna(subset=["country_name"], inplace=True)
        # dff.dropna(subset=[concentration], inplace=True)
    # Convert all country names to strings (made some problems if not)
    country_names = dff["country_name"].astype(str).unique()
    return [{"label": country, "value": country} for country in sorted(country_names)]


# Here is where the magic is made


@callback(
    Output(component_id="globe", component_property="figure"),
    Input(component_id="country", component_property="value"),
    Input(component_id="station", component_property="value"),
    Input(component_id="concentration-selector", component_property="value"),
)

# representation of a globe, different configurations are made in function of the inputs


def globe_representation(country_to_zoom, station, concentration):
    dff = whodata.df
    # If there is no concentration chosen, there is a simple globe represented
    if concentration is None:
        fig = px.scatter_geo(
            pd.DataFrame({"latitude": [], "longitude": []}),
            lat="latitude",
            lon="longitude",
            projection="orthographic",
        )
        # Update colors and globe
        fig.update_geos(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="LightGrey",
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showrivers=True,
            rivercolor="Blue",
        )
        fig.update_layout(
            title="3D globe",
            width=1000,
            height=800,
        )
    else:

        # sort years for the bar and drop Nan values of concentration for further processing
        dff = dff.sort_values(by="year_int", ascending=True)
        dff.dropna(subset=[concentration], inplace=True)

    # plot the concentrations without centering and specify station on the 3D globe
    if (country_to_zoom is None) and (station is None) and (concentration is not None):
        # plot points by their size and color in function of the concentration
        fig = px.scatter_geo(
            dff,
            lat="latitude",
            lon="longitude",
            size=concentration,
            color=concentration,
            animation_frame="year_int",
            projection="orthographic",
            color_continuous_scale="Viridis",
        )

        # Update colors and globe
        fig.update_geos(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="LightGrey",
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showrivers=True,
            rivercolor="Blue",
        )
        fig.update_layout(
            title=f"{concentration} over the years on a 3D globe",
            width=1000,
            height=800,
        )

    # show globe with concentration over all stations focused on one country
    elif (
        (country_to_zoom is not None)
        and (station is None)
        and (concentration is not None)
    ):

        # get coordinates to zoom the on the map the country of interest
        index = filtered_countries[
            filtered_countries["country_name"] == str(country_to_zoom)
        ].index
        # Get the latitude and longitude coordinates of the first row (by default)

        coordinates = filtered_countries.loc[index[0], ["latitude", "longitude"]]

        center_lat = coordinates["latitude"]
        center_lon = coordinates["longitude"]

        # plot points by their size and color in function of the concentration
        fig = px.scatter_geo(
            dff,
            lat="latitude",
            lon="longitude",
            size=concentration,
            color=concentration,
            animation_frame="year_int",
            projection="natural earth",
            color_continuous_scale="Viridis",
        )

        # Update colors and globe and center on wished country
        fig.update_geos(
            center=dict(lat=center_lat, lon=center_lon),
            projection_scale=5,
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="LightGrey",
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showrivers=True,
            rivercolor="Blue",
        )

        # Contour the chosed country in red
        fig.add_trace(
            go.Choropleth(
                locations=[country_to_zoom],
                locationmode="country names",
                z=[0],  # Dummy variable for color scale
                colorscale=[[0, "LightGrey"], [1, "LightGrey"]],
                showscale=False,
                marker=dict(line=dict(width=2, color="red")),
            )
        )

        fig.update_layout(
            title=f"{concentration} over the years centered on {country_to_zoom} on a 2D world map",
            width=1000,
            height=800,
        )

    # show globe with station and concentration without to zoom on a country
    elif (
        (country_to_zoom is None)
        and (station is not None)
        and (concentration is not None)
    ):
        dff.dropna(subset=["type_of_stations"], inplace=True)
        dff = dff[dff["type_of_stations"] == str(station)]

        fig = px.scatter_geo(
            dff,
            lat="latitude",
            lon="longitude",
            size=concentration,
            color=concentration,
            animation_frame="year_int",
            projection="orthographic",
            color_continuous_scale="Viridis",
        )

        # Update colors and globe
        fig.update_geos(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="LightGrey",
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showrivers=True,
            rivercolor="Blue",
        )
        fig.update_layout(
            title=f"{concentration} on {station} station over the years on a 3D globe",
            width=1000,
            height=800,
        )

    # show globe when every input is chosen
    elif (
        (country_to_zoom is not None)
        and (station is not None)
        and (concentration is not None)
    ):

        # get coordinates to zoom the on the map the country of interest
        index = filtered_countries[
            filtered_countries["country_name"] == str(country_to_zoom)
        ].index
        # Get the latitude and longitude coordinates of the first row (by default)

        coordinates = filtered_countries.loc[index[0], ["latitude", "longitude"]]

        dff.dropna(subset=["type_of_stations"], inplace=True)
        dff = dff[dff["type_of_stations"] == str(station)]

        center_lat = coordinates["latitude"]
        center_lon = coordinates["longitude"]

        # plot points by their size and color in function of the concentration
        fig = px.scatter_geo(
            dff,
            lat="latitude",
            lon="longitude",
            size=concentration,
            color=concentration,
            animation_frame="year_int",
            projection="natural earth",
            color_continuous_scale="Viridis",
        )

        # Update colors and globe in function of the country to zoom in
        fig.update_geos(
            center=dict(lat=center_lat, lon=center_lon),
            projection_scale=5,
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="LightGrey",
            showcountries=True,
            countrycolor="Black",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showrivers=True,
            rivercolor="Blue",
        )

        # Contour the chosed country in red
        fig.add_trace(
            go.Choropleth(
                locations=[country_to_zoom],
                locationmode="country names",
                z=[0],  # Dummy variable for color scale
                colorscale=[[0, "LightGrey"], [1, "LightGrey"]],
                showscale=False,
                marker=dict(line=dict(width=2, color="red")),
            )
        )

        fig.update_layout(
            title=f"{concentration} on {station} stations over the years centered on {country_to_zoom} on a 2D world map",
            width=1000,
            height=800,
        )

    return fig


@callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="graph-selector", component_property="value"),
)

# Make scatter with all datas to see the evoluton
# Also make boxplot


def update_graph(selected_value):
    if selected_value == "pm10_concentration":
        title = "mean PM10 value over the years"
    elif selected_value == "pm25_concentration":
        title = "mean PM25 value over the years"
    else:
        title = "mean NO2 value over the years"

    df_pivot = whodata.df.pivot_table(
        index="year", values=selected_value, aggfunc="mean"
    )

    fig = px.line(
        x=df_pivot.index,
        y=df_pivot[selected_value],
        labels={"x": "year", "y": selected_value},
        title=title,
    )
    return fig
