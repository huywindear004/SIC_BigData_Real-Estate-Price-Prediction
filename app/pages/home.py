import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [html.H2("Home Page"), html.P("Welcome to the Home Page!")],
    className="section-one container",
)
