from dash import html, dash_table, dcc, callback, Output, Input, State
import pandas as pd

# Add path to import root pakages
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/".join(i for i in current_dir.split("\\")[:-3]))

from modules.preprocessing.convert_modules import address_convert as ac

# Read data
df_init = pd.read_csv(
    "data/batdongsan/numerized/NhaO_numerized-dataset.csv", index_col=[0]
)
df_init.drop(columns=["Lat", "Long"], inplace=True)

df_init["Ward"] = df_init.apply(
    lambda row: ac.ward_deconvert(row["City"], row["District"], row["Ward"]), axis=1
)
df_init["District"] = df_init.apply(
    lambda row: ac.area_deconvert(row["City"], row["District"]), axis=1
)
df_init["City"] = df_init["City"].astype(pd.Int32Dtype()).apply(ac.region_deconvert)

house_dashboard_layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            ac.get_all_regions(),
                            placeholder="Select the region",
                            id="region-dropdown",
                        ),
                        dcc.Dropdown(placeholder="Select the area", id="area-dropdown"),
                        dcc.Dropdown(placeholder="Select the ward", id="ward-dropdown"),
                    ],
                    className="location-dropdowns",
                ),
                html.Button("Find", "find-btn", 0),
            ],
            className="location-menu",
        ),
        dash_table.DataTable(page_size=10, id="data-table"),
    ],
)


# ############ DROPDOWN UPDATE ############
# @callback(
#     Output("area-dropdown", "options"),
#     Input("region-dropdown", "value"),
#     prevent_initial_call=True,
# )
# def update_area_dropdown(reg_val):
#     if not reg_val:
#         return []
#     return ac.get_all_areas(reg_val)


# @callback(
#     Output("ward-dropdown", "options"),
#     Input("region-dropdown", "value"),
#     Input("area-dropdown", "value"),
#     prevent_initial_call=True,
# )
# def update_ward_dropdown(reg_val, are_val):
#     if not reg_val or not are_val:
#         return []
#     return ac.get_all_wards(reg_val, are_val)


# ############ TABLE UPDATE ############
# @callback(
#     Output("data-table", "data"),
#     Input("find-btn", "n_clicks"),
#     State("region-dropdown", "value"),
#     State("area-dropdown", "value"),
#     State("ward-dropdown", "value"),
#     prevent_initial_call=True,
# )
# def update_table(_, reg_val, are_val, war_val):
#     if reg_val is None:
#         return df_init.to_dict("records")
#     if are_val is None:
#         return df_init[df_init["City"] == reg_val].to_dict("records")
#     if war_val is None:
#         return df_init[
#             (df_init["City"] == reg_val) & (df_init["District"] == are_val)
#         ].to_dict("records")

#     return df_init[
#         (df_init["City"] == reg_val)
#         & (df_init["District"] == are_val)
#         & (df_init["Ward"] == war_val)
#     ].to_dict("records")
