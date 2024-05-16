import dash
from dash import Dash, html, dcc

app = Dash(
    __name__,
    title="Air Quality Dashboard",
    suppress_callback_exceptions=True,
    use_pages=True,
)


def main():

    app.layout = html.Div(
        [
            html.H1("Navigation Bar"),
            html.Div(
                [
                    html.Div(
                        dcc.Link(
                            f"{page['name']}",
                            href=page["relative_path"],
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            ),
            dash.page_container,
        ]
    )

    app.run_server(debug=False, port=8081)


if __name__ == "__main__":
    main()
