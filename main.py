from dash import Dash, html, dcc, dash_table, Input, Output, callback
from air_quality_dashboard import WHOData
from air_quality_dashboard import LocalData
import plotly.express as px

ITEMS_PER_PAGE = 10  # set the number of elements per page

app = Dash(__name__, title="Air Quality Dashboard", suppress_callback_exceptions=True)
whodata = WHOData.WHOData()
localdata = LocalData.LocalData()

# print("Debug: ")
# print(whodata.df.head())


def main():

    app.layout = html.Div(
        [
            html.Div(
                [
                    dcc.Link("Home", href="/"),
                    html.Span(" | "),
                    dcc.Link("Whodata statistics", href="/Whodata_statistics"),
                    html.Span(" | "),
                    dcc.Link("Localdata statistics", href="/Localdata_statistics"),
                ],
                style={"marginBottom": 10},
            ),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
        ]
    )

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/":
            return layout_home()
        elif pathname == "/Whodata_statistics":
            return layout_Whodatastatistics()
        elif pathname == "/Localdata_statistics":
            return layout_Localdatastatistics()
        else:
            return "404 Page Not Found"

    app.run_server(debug=True, port=8081)


def layout_home():
    return html.Div(
        [
            html.H1("Air Quality Dashboard"),
            html.P(
                "This dashboard shows air quality data from the WHO, as well as the NABEL database from Switzerland."
            ),
            html.H2("General Data"),
            html.H3("WHO Data"),
            html.P(
                f"Data from the following year is available: : {whodata.years[0]} - {whodata.years[-1]}"
            ),
            html.P(f"N° countries: {whodata.n_countries}"),
            html.H4("Data Table"),
            html.P(
                "This table shows the WHO data. Please use the =, >, <, >=, <=, != operators for filtering when using numbers. For the Country and type of station column the '=' operator has to be put in front of the word ('=Switzerland')"
            ),
            dash_table.DataTable(  # initalize the dash data table
                id="who_data",
                columns=[
                    {"id": "country_name", "name": "Country", "type": "text"},
                    {"id": "year_int", "name": "Year"},
                    {"id": "city", "name": "City"},
                    {"id": "pm10_concentration", "name": "PM10"},
                    {"id": "pm10_tempcov", "name": "PM10 Coverage"},
                    {"id": "pm25_concentration", "name": "PM25"},
                    {"id": "pm25_tempcov", "name": "PM25 Coverage"},
                    {"id": "no2_concentration", "name": "NO2"},
                    {"id": "no2_coverage", "name": "NO2 Coverage"},
                    {
                        "id": "type_of_stations",
                        "name": "Type of Station",
                        "type": "text",
                    },
                ],
                page_current=0,
                page_size=ITEMS_PER_PAGE,  # set the number of elements per page
                page_action="custom",
                filter_action="custom",
                filter_query="",
                sort_action="custom",
                sort_mode="multi",
                sort_by=[],
            ),
            html.H3("Switzerland Data"),
            html.P(f"First data entry from: {localdata.min_date()}"),
            html.P(f"Data last updated: {localdata.max_date()}"),
            html.H4("Data Table"),
            html.P(
                "This table shows the local data from Switzerland. Please use the =, >, <, >=, <=, != operators for filtering when using numbers. The Type of site, and the Location column can be filtered directly. "
            ),
            dash_table.DataTable(  # initalize the dash data table
                id="local_data_switzerland",
                columns=[
                    {
                        "name": i,
                        "id": i,
                        "deletable": True,
                    }  # use all columns from the local data (Switzerland)
                    for i in localdata.df.columns  # use all columns from the local data (Switzerland)
                ],
                page_current=0,
                page_size=ITEMS_PER_PAGE,  # set the number of elements per page
                page_action="custom",
                filter_action="custom",
                filter_query="",
                sort_action="custom",
                sort_mode="multi",
                sort_by=[],
            ),
        ]
    )


# Statistics page layout, for histogram graph. For the next task also graph would be nice.  Also add a third page with local_data


def layout_Whodatastatistics():

    # Filter the countries and years for the dropdown menu
    filtered_countries = whodata.df.drop_duplicates(subset="country_name")
    filtered_years = whodata.df.drop_duplicates(subset="year")

    dropdown_style = {"width": "200px"}

    return html.Div(
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


def layout_Localdatastatistics():
    return html.Div(
        [
            html.H1("Localdata Statistics"),
        ]
    )


# Operators translation table from the internal dash frontend syntax to the pandas syntax
operators = [
    ["ge ", ">="],
    ["le ", "<="],
    ["lt ", "<"],
    ["gt ", ">"],
    ["ne ", "!="],
    ["eq ", "="],
    ["contains "],
    ["datestartswith "],
]


def split_filter_part(filter_part):
    """
    Split filter function of dash in order to interpret their propriatary filter function of the frontend
    and then apply it to the data table.
    Directly taken from the dash documentation.
    https://dash.plotly.com/datatable/callbacks
    """
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find("{") + 1 : name_part.rfind("}")]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                    value = value_part[1:-1].replace("\\" + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


# Callback function to update the table based on sorting and filtering criteria, hence we have a data table
# that is updated based on backend operations.
# here we have the callback function for the local data
@callback(
    Output("local_data_switzerland", "data"),
    Input("local_data_switzerland", "page_current"),
    Input("local_data_switzerland", "page_size"),
    Input("local_data_switzerland", "sort_by"),
    Input("local_data_switzerland", "filter_query"),
)
def update_table_switzerland(page_current, page_size, sort_by, filter):
    # Split the filter query into individual filtering expressions
    filtering_expressions = filter.split(" && ")
    dff = localdata.df
    # Apply each filtering expression to the DataFrame
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(
            filter_part
        )  # split the filter part
        if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
            # Apply comparison operators to filter the DataFrame
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == "contains":
            if col_name in [
                "Type of site",
                "Location",
            ]:  # Workaround to avoid error when filtering on non-string columns. Not nice, should be fixed in the future.
                dff = dff.loc[dff[col_name].str.contains(filter_value, case=False)]
    if len(sort_by):  # Code to sort the data based on the chosen column
        dff = dff.sort_values(
            [col["column_id"] for col in sort_by],
            ascending=[col["direction"] == "asc" for col in sort_by],
            inplace=False,
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size : (page + 1) * size].to_dict(
        "records"
    )  # only hand the data of the current page to the webbrowser frontend


# same function as above, but for the WHO data
@app.callback(
    Output("who_data", "data"),
    Input("who_data", "page_current"),
    Input("who_data", "page_size"),
    Input("who_data", "sort_by"),
    Input("who_data", "filter_query"),
)
def update_table_whodata(page_current, page_size, sort_by, filter):
    # Split the filter query into individual filtering expressions
    filtering_expressions = filter.split(" && ")
    dff = whodata.df
    # dff["year"] = dff["year"].strftime("%Y")
    # Apply each filtering expression to the DataFrame
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(
            filter_part
        )  # split the filter part

        if operator == "contains":
            if col_name in ["Country", "Type of Station"]:
                # Workaround to avoid error when filtering on non-string columns. Not nice, should be fixed in the future.
                dff = dff.loc[dff[col_name].str.contains(filter_value, case=False)]

        elif operator in ("eq", "ne", "lt", "le", "gt", "ge"):
            # Apply comparison operators to filter the DataFrame
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]

    if len(sort_by):  # Code to sort the data based on the chosen column
        dff = dff.sort_values(
            [col["column_id"] for col in sort_by],
            ascending=[col["direction"] == "asc" for col in sort_by],
            inplace=False,
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size : (page + 1) * size].to_dict(
        "records"
    )  # only hand the data of the current page to the webbrowser frontend


# Statitics, represent with histograms and graphs


# Histogramm which presents the max values in function of the country
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


# Histogramm which presents different values in function of the region


@callback(
    Output(component_id="histogram-graph", component_property="figure"),
    Input(component_id="histogram-selector", component_property="value"),
)
def update_histogramm(selected_value):
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


if __name__ == "__main__":
    main()
