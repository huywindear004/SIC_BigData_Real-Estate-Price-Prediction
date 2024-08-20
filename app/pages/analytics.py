import dash
from dash import html, dash_table, dcc, callback, Output, Input, State

from pages.analytics_pages import (
    analytics_apartment,
    analytics_house,
    analytics_land,
)

dash.register_page(
    __name__,
    path="/analytics-dashboard",
    name="Analytics Dashboard",
    title="Analytics Dashboard",
)

layout = html.Div(
    [
        html.H1("Analytics page"),
        dcc.Tabs(
            [
                dcc.Tab(label="Land", value="land-tab"),
                dcc.Tab(label="House", value="house-tab"),
                dcc.Tab(label="Apartment", value="apartment-tab"),
            ],
            id="analytics-tabs",
        ),
        html.Div(["This is tab content"], id="analytics-content"),
    ],
    className="container",
)


@callback(
    Output("analytics-content", "children"),
    Input("analytics-tabs", "value"),
    prevent_initial_call=True,
)
def render_analytics_content(tab_value):
    if tab_value == "land-tab":
        return "This is land"
    if tab_value == "house-tab":
        return analytics_house.house_dashboard_layout
    if tab_value == "apartment-tab":
        return "This is apart"
