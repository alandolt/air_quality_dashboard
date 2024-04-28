from dash import Dash, html, dcc
from air_quality_dashboard import WHOData

app = Dash(__name__)
whodata = WHOData.WHOData()

def main():

    print("Debug: ")
    print(whodata.df.head())
    
    app.layout = html.Div(
        [
            html.H1("Air Quality Dashboard"),
            html.P("This dashboard shows air quality data from the WHO."),
            html.H2("General Statistics"),
            html.P(
                f"First and last year of records: {whodata.years[0]}, {whodata.years[-1]}"
            ),
            html.P(
                f"N° countries: {whodata.n_countries}"
            ),
        ]
    )
    app.run(debug=True, port=8080)


if __name__ == "__main__":
    main()
