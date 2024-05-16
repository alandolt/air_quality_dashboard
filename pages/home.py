"""
Dash Page for start page, including a data table for the localdata, as well as the WHO data. 
Further, some small statistics regarding the dataset are shown. 
"""

import dash
from dash import html, dash_table, Input, Output, callback
from air_quality_dashboard.dashboard import helper_functions
from air_quality_dashboard.data_parser import who_data
from air_quality_dashboard.data_parser import local_data

dash.register_page(__name__, path="/", name="Home")


ITEMS_PER_PAGE = 10  # set the number of elements per page
whodata = who_data.WHOData()
localdata = local_data.LocalData()

layout = html.Div(
    [
        html.H1("Air Quality Dashboard"),
        html.P(
            "This dashboard shows air quality data from the WHO, as well as the \
                NABEL database from Switzerland."
        ),
        html.H2("General Data"),
        html.H3("WHO Data"),
        html.P(
            f"Data from the following year is available: :  \
                    {whodata.years[0]} - {whodata.years[-1]}"
        ),
        html.P(f"N° countries: {whodata.n_countries}"),
        html.H4("Data Table"),
        html.P(
            "This table shows the WHO data. Please use the =, >, <, >=, <=, != operators for filtering when using numbers.  \
                    For the Country and type of station column the '=' operator has to be put in front of the word ('=Switzerland')"
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
            "This table shows the local data from Switzerland.  \
                    Please use the =, >, <, >=, <=, != operators for filtering when using numbers.  \
                        The Type of site, and the Location column can be filtered directly. "
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
def update_table_switzerland(
    page_current,
    page_size,
    sort_by,
    filter,
):
    # Split the filter query into individual filtering expressions
    filtering_expressions = filter.split(" && ")
    dff = localdata.df
    # Apply each filtering expression to the DataFrame
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = helper_functions.split_filter_part(
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
@callback(
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
        col_name, operator, filter_value = helper_functions.split_filter_part(
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
