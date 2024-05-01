from dash import Dash, html, dcc, dash_table
from air_quality_dashboard import WHOData
from air_quality_dashboard import LocalData

app = Dash(__name__)
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
            html.H3("Switzerland Data"),
            html.P(f"First data entry from: {localdata.min_date()}"),
            html.P(f"Data last updated: {localdata.max_date()}"),
        ]
    )
    app.run(debug=True, port=8080)


if __name__ == "__main__":
    main()
