# import dash
# from dash import html, dcc, callback, Input, Output, State
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# from modules.preprocessing.convert_modules import (
#     address_convert as ac,
#     others_convert as oc,
# )

# # dash.register_page(__name__, path="/predicting/house", title="Predict House Price")


# scaler = joblib.load(open("models/house_scaler.pkl", "rb"))

# house_model = joblib.load(open("models/house_stacking_model.pkl", "rb"))

# layout = html.Div(
#     [
#         html.H3("City"),
#         dcc.Dropdown(
#             ac.get_all_regions(),
#             placeholder="Select the region",
#             id="region-dropdown",
#         ),
#         html.H3("Area"),
#         dcc.Dropdown(placeholder="Select the area", id="area-dropdown"),
#         html.H3("Ward"),
#         dcc.Dropdown(placeholder="Select the ward", id="ward-dropdown"),
#         html.H3("Enter size: "),
#         dcc.Input(type="number", className="Select-control", id="house-size-input"),
#         html.H3("Enter facade: "),
#         dcc.Input(
#             type="number",
#             className="Select-control",
#             id="house-facade-input",
#         ),
#         html.H3("Choose legal status: "),
#         dcc.Dropdown(
#             oc.get_all_legal_status(),
#             placeholder="Select legal status of property",
#             id="house-legalty-input",
#         ),
#         html.H3("Choose furnishment status: "),
#         dcc.Dropdown(
#             oc.get_all_furnishment(),
#             placeholder="Select furnishment status of property",
#             id="house-furnishiment-input",
#         ),
#         html.H3("Choose direction: "),
#         dcc.Dropdown(
#             oc.get_all_directions(),
#             placeholder="Select the direction of property",
#             id="house-direction-input",
#         ),
#         html.H3("Enter number of bedrooms: "),
#         dcc.Input(type="number", className="Select-control", id="house-bedroom-input"),
#         html.H3("Enter number of toilets: "),
#         dcc.Input(type="number", className="Select-control", id="house-toilet-input"),
#         html.H3("Enter the way-in length: "),
#         dcc.Input(type="number", className="Select-control", id="house-wayin-input"),
#         html.H3("Enter the number of floors: "),
#         dcc.Input(type="number", className="Select-control", id="house-floor-input"),
#         html.Div(
#             [
#                 html.H2([], id="price_predicted"),
#                 html.Button("Predict", "predict-btn", n_clicks=0),
#             ],
#             className="row",
#         ),
#     ]
# )


# @callback(
#     Output("price_predicted", "children"),
#     State("region-dropdown", "value"),
#     State("area-dropdown", "value"),
#     State("ward-dropdown", "value"),
#     State("house-size-input", "value"),
#     State("house-facade-input", "value"),
#     State("house-legalty-input", "value"),
#     State("house-furnishiment-input", "value"),
#     State("house-direction-input", "value"),
#     State("house-bedroom-input", "value"),
#     State("house-toilet-input", "value"),
#     State("house-wayin-input", "value"),
#     State("house-floor-input", "value"),
#     Input("predict_btn", "n_clicks"),
#     prevent_initial_call=True,
# )
# def predict_house_price(
#     reg_id,
#     are_id,
#     war_id,
#     size,
#     facade,
#     legalty,
#     furni,
#     dir,
#     bedr,
#     toil,
#     wayin,
#     floor,
#     click,
# ):
#     input = {
#         "DienTich": [size],
#         "City": [reg_id],
#         "District": [are_id],
#         "MatTien": [facade],
#         "PhapLy": [legalty],
#         "DuongVao": [wayin],
#         "HuongNha": [dir],
#         "SoTang": [floor],
#         "SoPhongNgu": [bedr],
#         "SoToilet": [toil],
#         "NoiThat": [furni],
#         "Ward": [war_id],
#     }
#     df = pd.DataFrame(input)
#     df.fillna([np.nan], inplace=True)
#     print("cc")
#     return house_model.predict(scaler.transform(df))[0]
