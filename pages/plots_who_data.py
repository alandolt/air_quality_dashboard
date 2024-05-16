# Statistics page layout, for histogram graph.
# For the next task also graph would be nice.  Also add a third page with local_data

import dash
from dash import html, Input, Output, callback, dcc
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
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

dropdown_style_year = {"width": "200px"}
dropdown_style_country = {"width": "600px"}

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
        # Selection with buttons for different concentrations for bar plotting
        html.H2(
            "See mean values in function of the region and concentration (just for fun)"
        ),
        dcc.RadioItems(
            id="bar-selector",
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
        dcc.Graph(id="bar-graph"),
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
