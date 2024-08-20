# Import packages
import dash
from dash import Dash, html, dcc, clientside_callback, Input, Output, State
import dash_bootstrap_components as dbc

from components.sidebar import sidebar

# Initialize the app
app = Dash(
    __name__,
    title="Real Estate Price Prediction",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
    use_pages=True,
)


app.layout = html.Div(
    [
        sidebar(),
        html.Div(
            [
                html.H1(
                    "SAMSUNG INNOVATION CAMPUS CAPSTONE PROJECT",
                    "header",
                    className="header",
                ),
                dash.page_container,
            ],
            id="main",
            className="collapsed-sidebar",
        ),
        # Store for sidebar state
        dcc.Store(id="sidebar-toggle-state", data={"expanded": False}),
    ]
)


# Clientside callback to handle sidebar toggle
app.clientside_callback(
    """
    function(n_clicks, data) {
        const sidebar = document.getElementById('sidebar');
        const icon = document.getElementById('sidebar-toggle-icon');
        const main = document.getElementById('main');

        if (data.expanded) {
            sidebar.classList.remove('expanded');
            sidebar.classList.add('collapsed');
            icon.classList.remove('rotate');
            main.classList.remove('expanded-sidebar')
            main.classList.add('collapsed-sidebar')
            return {'expanded': false};
        } else {
            sidebar.classList.remove('collapsed');
            sidebar.classList.add('expanded');
            icon.classList.add('rotate');
            main.classList.remove('collapsed-sidebar')
            main.classList.add('expanded-sidebar')
            return {'expanded': true};
        }
    }
    """,
    Output("sidebar-toggle-state", "data"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-toggle-state", "data"),
    prevent_initial_call=True,
)

# Run the app
if __name__ == "__main__":
    app.run()
