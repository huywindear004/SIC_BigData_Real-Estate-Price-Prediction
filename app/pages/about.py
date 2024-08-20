import dash
from dash import html

dash.register_page(__name__, path="/about")

layout = html.Div(
    [html.H2("About Page"), html.P("Welcome to the About Page!")], className="container"
)
