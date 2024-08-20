from dash import html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import seaborn as sns

# Add path to import root pakages
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/".join(i for i in current_dir.split("\\")[:-3]))

from modules.preprocessing.convert_modules import address_convert as ac

# Read data
df_raw = pd.read_csv(
    "data/batdongsan/numerized/NhaO_numerized-dataset.csv", index_col=[0]
)
df_init = df_raw.drop(columns=["Lat", "Long"])
df_init.dropna(subset=["City", "District", "Ward"], inplace=True)


df_init["Ward"] = df_init.apply(
    lambda row: ac.ward_deconvert(row["City"], row["District"], row["Ward"]), axis=1
)
df_init["District"] = df_init.apply(
    lambda row: ac.area_deconvert(row["City"], row["District"]), axis=1
)
df_init["City"] = df_init["City"].astype(pd.Int32Dtype()).apply(ac.region_deconvert)

house_dashboard_layout = html.Div(
    [],
)
