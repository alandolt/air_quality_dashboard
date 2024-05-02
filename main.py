from dash import Dash, html, dcc, dash_table, Input, Output, callback
from air_quality_dashboard import WHOData
from air_quality_dashboard import LocalData

ITEMS_PER_PAGE = 10  # set the number of elements per page

app = Dash(__name__, title="Air Quality Dashboard")
whodata = WHOData.WHOData()
localdata = LocalData.LocalData()


def main():

    print("Debug: ")
    print(whodata.df.head())

    app.layout = html.Div(
        [
            html.H1("Air Quality Dashboard"),
            html.P(
                "This dashboard shows air quality data from the WHO, as well as the NABEL database from Switzerland."
            ),
            html.H2("General Statistics"),
            html.H3("WHO Data"),
            html.P(
                f"Data from the following year is available: : {whodata.years[0]} - {whodata.years[-1]}"
            ),
            html.P(f"N° countries: {whodata.n_countries}"),
            html.H4("Data Table"),
            html.P(
                "This table shows the WHO data. Please use the =, >, <, >=, <=, != operators for filtering when using numbers. The Country column can be filtered directly. "
            ),
            dash_table.DataTable(  # initalize the dash data table
                id="who_data",
                columns=[
                    {"id": "country_name", "name": "Country"},
                    {"id": "year_int", "name": "Year"},
                    {"id": "city", "name": "City"},
                    {"id": "pm10_concentration", "name": "PM10"},
                    {"id": "pm10_tempcov", "name": "PM10 Coverage"},
                    {"id": "pm25_concentration", "name": "PM25"},
                    {"id": "pm25_tempcov", "name": "PM25 Coverage"},
                    {"id": "no2_concentration", "name": "NO2"},
                    {"id": "no2_coverage", "name": "NO2 Coverage"},
                    {"id": "type_of_stations", "name": "Type of Station"},
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
    app.run(debug=True, port=8080)


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
        col_name, operator, filter_value = split_filter_part(
            filter_part
        )  # split the filter part
        if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
            # Apply comparison operators to filter the DataFrame
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == "contains":
            if col_name in [
                "Country"
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


if __name__ == "__main__":
    main()
