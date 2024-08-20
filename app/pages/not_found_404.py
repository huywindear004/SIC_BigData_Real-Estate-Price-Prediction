import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(
    [
        html.Div(
            html.Img(
                src="assets/img/404_error_message.svg",
                className="col-12 col-md-4",
                alt="404 Error Message",
            ),
            className="row justify-content-center",
        ),
        html.Div(
            [
                dbc.Button(
                    "Go Home!",
                    class_name="btn btn-primary btn-lg col-12 col-md-6",
                    href="/",
                ),
            ],
            className="row justify-content-center",
        ),
    ],
    className="container",
)
