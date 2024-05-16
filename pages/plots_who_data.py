# Statistics page layout, for histogram graph.
# For the next task also graph would be nice.  Also add a third page with local_data

import dash
from dash import html, Input, Output, callback, dcc
import plotly.express as px
from air_quality_dashboard.data_parser import who_data

dash.register_page(__name__, path="/whodata", name="Plots WHO data")


ITEMS_PER_PAGE = 10  # set the number of elements per page
whodata = who_data.WHOData()

# Filter the countries and years for the dropdown menu
filtered_countries = whodata.df.drop_duplicates(subset="country_name")
filtered_years = whodata.df.drop_duplicates(subset="year")

dropdown_style = {"width": "200px"}

layout = html.Div(
    [
        html.H1("WHOdata Statistics"),
        # Dropdown menus to chose different countries and their corresponding max_value in a certain timespan
        # Dropdown menus for years
        html.H2(
            "See max values in function of the country, timespan and concentration"
        ),
        html.Div(
            [
                html.H5("Year 1"),
                dcc.Dropdown(
                    id="year-1",
                    options=sorted(filtered_years["year"]),
                    value=filtered_years["year"].iloc[0],
                    style=dropdown_style,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.H5("Year 2"),
                dcc.Dropdown(
                    id="year-2",
                    options=sorted(filtered_years["year"]),
                    value=filtered_years["year"].iloc[0],
                    style=dropdown_style,
                ),
            ],
            style={"display": "inline-block"},
        ),
        # Dropdown menu for countrys
        html.Div(
            [
                html.H5("Country 1"),
                dcc.Dropdown(
                    id="country-1",
                    options=sorted(filtered_countries["country_name"]),
                    value=filtered_countries["country_name"].iloc[0],
                    style=dropdown_style,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.H5("Country 2"),
                dcc.Dropdown(
                    id="country-2",
                    options=sorted(filtered_countries["country_name"]),
                    value=filtered_countries["country_name"].iloc[0],
                    style=dropdown_style,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Div(
            [
                html.H5("Country 3"),
                dcc.Dropdown(
                    id="country-3",
                    options=sorted(filtered_countries["country_name"]),
                    value=filtered_countries["country_name"].iloc[0],
                    style=dropdown_style,
                ),
            ],
            style={"display": "inline-block"},
        ),
        html.Br(),  # don't work, no space is made
        dcc.RadioItems(
            id="histogram-max-selector",
            options=[
                {"label": "PM10", "value": "pm10_concentration"},
                {"label": "PM25", "value": "pm25_concentration"},
                {"label": "NO2", "value": "no2_concentration"},
                {"label": "PM10 Coverage", "value": "pm10_tempcov"},
                {"label": "PM25 Coverage", "value": "pm25_tempcov"},
                {"label": "NO2 Coverage", "value": "no2_tempcov"},
            ],
            value="pm10_concentration",
            labelStyle={"display": "inline-block"},
        ),
        # Put a histogramm for the max values
        dcc.Graph(id="histogram-max"),
        # Selection with buttons for different concentrations for histogram plotting
        html.H2("See mean values in function of the region and concentration"),
        dcc.RadioItems(
            id="histogram-selector",
            options=[
                {"label": "PM10", "value": "pm10_concentration"},
                {"label": "PM25", "value": "pm25_concentration"},
                {"label": "NO2", "value": "no2_concentration"},
                {"label": "PM10 Coverage", "value": "pm10_tempcov"},
                {"label": "PM25 Coverage", "value": "pm25_tempcov"},
                {"label": "NO2 Coverage", "value": "no2_tempcov"},
            ],
            value="pm10_concentration",
            labelStyle={"display": "inline-block"},
        ),
        dcc.Graph(id="histogram-graph"),
        html.H2("See mean concentration of all countries over the years"),
        # Selection with dropdown menu for different concentrations for graph plotting
        dcc.Dropdown(
            id="graph-selector",
            options=[
                {"label": "PM10", "value": "pm10_concentration"},
                {"label": "PM25", "value": "pm25_concentration"},
                {"label": "NO2", "value": "no2_concentration"},
                {"label": "PM10 Coverage", "value": "pm10_tempcov"},
                {"label": "PM25 Coverage", "value": "pm25_tempcov"},
                {"label": "NO2 Coverage", "value": "no2_tempcov"},
            ],
            value="pm10_concentration",
        ),
        dcc.Graph(id="graph"),
    ]
)


@callback(
    Output(component_id="histogram-max", component_property="figure"),
    Input(component_id="histogram-max-selector", component_property="value"),
    Input(component_id="country-1", component_property="value"),
    Input(component_id="country-2", component_property="value"),
    Input(component_id="country-3", component_property="value"),
    Input(component_id="year-1", component_property="value"),
    Input(component_id="year-2", component_property="value"),
)
def update_histogram_max(
    selected_value, country_1, country_2, country_3, year_1, year_2
):
    """
    Histogramm which presents the max values in function of the country

    """
    if selected_value == "pm10_concentration":
        title = "PM10 Concentration"
    elif selected_value == "pm25_concentration":
        title = "PM25 Concentration"
    elif selected_value == "no2_concentration":
        title = "NO2 Concentration"
    elif selected_value == "pm10_tempcov":
        title = "PM10 Coverage"
    elif selected_value == "pm25_tempcov":
        title = "PM25 Coverage"
    else:
        title = "NO2 Coverage"

    df = whodata.df[(whodata.df["year"] <= year_1) & (whodata.df["year"] <= year_2)]

    max_country_1 = df[df["country_name"] == country_1][selected_value].max()
    max_country_2 = df[df["country_name"] == country_2][selected_value].max()
    max_country_3 = df[df["country_name"] == country_3][selected_value].max()

    fig = px.histogram(
        x=[country_1, country_2, country_3],
        y=[max_country_1, max_country_2, max_country_3],
        title=title,
        labels={"x": "Country", "y": selected_value},
        color_discrete_sequence=["orange"],
    )

    return fig


@callback(
    Output(component_id="histogram-graph", component_property="figure"),
    Input(component_id="histogram-selector", component_property="value"),
)
def update_histogramm(selected_value):
    """
    Histogramm which presents different values in function of the region
    """
    if selected_value == "pm10_concentration":
        title = "mean PM10 value over the years"
    elif selected_value == "pm25_concentration":
        title = "mean PM25 value over the years"
    elif selected_value == "no2_concentration":
        title = "mean NO2 value over the years"
    elif selected_value == "pm10_tempcov":
        title = "mean PM10 Coverage over the years"
    elif selected_value == "pm25_tempcov":
        title = "mean PM25 Coverage over the years"
    else:
        title = "mean NO2 Coverage over the years"

    whodata.df["type_of_stations"] = whodata.df["type_of_stations"].str.replace(
        ",", " "
    )
    whodata.df["type_of_stations"] = whodata.df["type_of_stations"].str.split().str[0]

    df_pivot = whodata.df.pivot_table(
        index="type_of_stations", values=selected_value, aggfunc="mean"
    )
    fig = px.histogram(
        df_pivot,
        x=df_pivot.index,
        y=df_pivot[selected_value],
        labels={"x": "Type of Station", "y": selected_value},
        title=title,
    )

    return fig


@callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="graph-selector", component_property="value"),
)
def update_graph(selected_value):
    if selected_value == "pm10_concentration":
        title = "mean PM10 value over the years"
    elif selected_value == "pm25_concentration":
        title = "mean PM25 value over the years"
    elif selected_value == "no2_concentration":
        title = "mean NO2 value over the years"
    elif selected_value == "pm10_tempcov":
        title = "mean PM10 Coverage over the years"
    elif selected_value == "pm25_tempcov":
        title = "mean PM25 Coverage over the years"
    else:
        title = "mean NO2 Coverage over the years"

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
