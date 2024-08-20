from dash import html
import dash_bootstrap_components as dbc


def sidebar():
    return html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fa-solid fa-house"), html.Span("Home")],
                        href="/",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fa-solid fa-chart-line"),
                            html.Span("Analytics"),
                        ],
                        href="/analytics-dashboard",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fa-solid fa-map-location-dot"),
                            html.Span("Map"),
                        ],
                        href="/map",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fa-solid fa-coins"),
                            html.Span("Price Predicting"),
                        ],
                        href="/predicting",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="fa-solid fa-circle-info"),
                            html.Span("About"),
                        ],
                        href="/about",
                        active="exact",
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            html.Button(
                html.I(
                    id="sidebar-toggle-icon",
                    className="fa-solid fa-arrow-right-from-bracket",
                ),
                "sidebar-toggle",
                className="sidebar__mode-btn",
            ),
        ],
        "sidebar",
        className="sidebar collapsed",
    )
