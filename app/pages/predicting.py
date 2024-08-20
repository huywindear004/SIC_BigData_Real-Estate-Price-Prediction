import dash
from dash import html, dcc, callback, Input, Output, State
import joblib
import numpy as np
import pandas as pd

from modules.preprocessing.convert_modules import (
    address_convert as ac,
    others_convert as oc,
)


dash.register_page(__name__, path="/predicting", title="Price Predicting")

scaler = joblib.load(open("models/house_scaler.pkl", "rb"))

house_model = joblib.load(open("models/house_stacking_model.pkl", "rb"))

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    [html.I(className="fa-solid fa-city"), "City"],
                                    className="input-label",
                                ),
                                dcc.Dropdown(
                                    ac.get_all_regions(),
                                    placeholder="Select the region",
                                    id="region-dropdown",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(["Area"], className="input-label"),
                                dcc.Dropdown(
                                    placeholder="Select the area", id="area-dropdown"
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(["Ward"], className="input-label"),
                                dcc.Dropdown(
                                    placeholder="Select the ward", id="ward-dropdown"
                                ),
                            ],
                            className="col-4",
                        ),
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-maximize"),
                                        "Enter size: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Input(
                                    type="number",
                                    className="Select-control",
                                    id="house-size-input",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(
                                            className="fa-solid fa-arrows-left-right-to-line"
                                        ),
                                        "Enter facade: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Input(
                                    type="number",
                                    className="Select-control",
                                    id="house-facade-input",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-arrow-turn-up"),
                                        "Enter the way-in length: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Input(
                                    type="number",
                                    className="Select-control",
                                    id="house-wayin-input",
                                ),
                            ],
                            className="col-4",
                        ),
                    ],
                    className="row",
                ),
                html.H3(
                    [
                        html.I(className="fa-solid fa-layer-group"),
                        "Enter the number of floors: ",
                    ],
                    className="input-label",
                ),
                dcc.Input(
                    type="number", className="Select-control", id="house-floor-input"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-bed"),
                                        "Enter number of bedrooms: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Input(
                                    type="number",
                                    className="Select-control",
                                    id="house-bedroom-input",
                                ),
                            ],
                            className="col-6",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-toilet-portable"),
                                        "Enter number of toilets: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Input(
                                    type="number",
                                    className="Select-control",
                                    id="house-toilet-input",
                                ),
                            ],
                            className="col-6",
                        ),
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-scale-balanced"),
                                        "Choose legal status: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Dropdown(
                                    oc.get_all_legal_status(),
                                    placeholder="Select legal status of property",
                                    id="house-legalty-input",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-chair"),
                                        "Choose furnishment status: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Dropdown(
                                    oc.get_all_furnishment(),
                                    placeholder="Select furnishment status of property",
                                    id="house-furnishiment-input",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [
                                html.H3(
                                    [
                                        html.I(className="fa-solid fa-location-arrow"),
                                        "Choose direction: ",
                                    ],
                                    className="input-label",
                                ),
                                dcc.Dropdown(
                                    oc.get_all_directions(),
                                    placeholder="Select the direction of property",
                                    id="house-direction-input",
                                ),
                            ],
                            className="col-4",
                        ),
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Button(
                            "Predict",
                            id="predict-btn",
                            n_clicks=0,
                            className="col-12 btn btn-primary btn-lg btn-block",
                        ),
                        html.H2([], id="price_predicted", className="col-12"),
                    ],
                ),
            ]
        )
    ],
    className="container",
)


# layout = html.Div(
#     [
#         html.Div(
#             [
#                 html.H2("Type of property"),
#                 dcc.Tabs(
#                     [
#                         dcc.Tab(label="Land", value="land-tab"),
#                         dcc.Tab(
#                             label="House",
#                             value="house-tab",
#                         ),
#                         dcc.Tab(label="Apartment", value="apartment-tab"),
#                     ],
#                     id="predicting-tabs",
#                 ),
#             ]
#         ),
#         html.Div(id="predicting_content"),
#     ],
#     className="container",
# )


# @callback(
#     Output("predicting_content", "children"),
#     Input("predicting-tabs", "value"),
#     prevent_initial_call=True,
# )
# def render_predicting_content(type):
#     if type == "house-tab":
#         return predicting_house.layout
#     if type == "Land":
#         return
#     if type == "Apartment":
#         return


@callback(
    Output("price_predicted", "children"),
    State("region-dropdown", "value"),
    State("area-dropdown", "value"),
    State("ward-dropdown", "value"),
    State("house-size-input", "value"),
    State("house-facade-input", "value"),
    State("house-legalty-input", "value"),
    State("house-furnishiment-input", "value"),
    State("house-direction-input", "value"),
    State("house-bedroom-input", "value"),
    State("house-toilet-input", "value"),
    State("house-wayin-input", "value"),
    State("house-floor-input", "value"),
    Input("predict-btn", "n_clicks"),
    prevent_initial_call=True,
)
def predict_house_price(
    reg_id,
    are_id,
    war_id,
    size,
    facade,
    legalty,
    furni,
    dir,
    bedr,
    toil,
    wayin,
    floor,
    click,
):
    input = {
        "DienTich": [size],
        "City": [reg_id],
        "District": [are_id],
        "MatTien": [facade],
        "PhapLy": [legalty],
        "DuongVao": [wayin],
        "HuongNha": [dir],
        "SoTang": [floor],
        "SoPhongNgu": [bedr],
        "SoToilet": [toil],
        "NoiThat": [furni],
        "Ward": [war_id],
    }
    df = pd.DataFrame(input)
    df.fillna(np.nan, inplace=True)
    usd = int(round(house_model.predict(scaler.transform(df))[0], 0))
    return "{:,}".format(usd) + " $ ~ " + "{:,}".format(usd * 25_000) + " VND"


#
@callback(
    Output("area-dropdown", "options"),
    Input("region-dropdown", "value"),
    prevent_initial_call=True,
)
def update_area_dropdown(reg_id):
    if reg_id is None:
        return []
    return ac.get_all_areas(reg_id)


@callback(
    Output("ward-dropdown", "options"),
    Input("region-dropdown", "value"),
    Input("area-dropdown", "value"),
    prevent_initial_call=True,
)
def update_ward_dropdown(reg_id, are_id):
    if reg_id is None or are_id is None:
        return []
    return ac.get_all_wards(reg_id, are_id)
