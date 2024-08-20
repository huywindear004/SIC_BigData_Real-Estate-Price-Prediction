import json
import re
import pandas as pd
import os
from unidecode import unidecode


def __get_place_name(full_name):
    """
    ## Return a lowercase non-accent plain name of a location in Viet Nam
    E.g.:
    - 'Thành phố Hồ Chí Minh' -> hochiminh
    - 'Tỉnh Nam Định' -> namdinh
    - 'Thủ Đức (Quận 9 cũ)' -> thuduc
    """
    if pd.isna(full_name):
        return pd.NA
    # Remove parentheses
    if "(" in full_name:
        full_name = re.sub(r"\(.*?\)", "", full_name)
    # Replace administrative unit strings
    no_unit_name = re.sub(
        r"\A(thành phố|tp|tỉnh|huyện|quận|thị xã|xã|phường|thị trấn|xả|tĩnh)",
        "",
        full_name.strip().lower(),
    )
    plain = re.sub(r"[^a-z0-9]", "", unidecode(no_unit_name))
    # Convert 009 -> 9, 0003->3
    if plain.isnumeric():
        return str(int(plain))
    return plain


def __extract_ward(address: str):
    """
    Extract the ward, ward, or commune from the given address.
    E.g.:
    - 'Dự án Vinhomes Green Bay Mễ Trì, Đường Đại lộ Thăng Long, Phường Mễ Trì, Nam Từ Liêm, Hà Nội'
      -> 'Phường Mễ Trì'
    - 'Dự án Vinhomes Green Bay Mễ Trì, Đường Đại lộ Thăng Long, Nam Từ Liêm, Hà Nội'
      -> None
    """
    if pd.isna(address):
        return pd.NA
    match = re.search(r"\b(Phường|Xã|Thị trấn)\s+[^,]+", address, re.IGNORECASE)

    if match:
        return match.group(0).strip()
    return pd.NA


def __region_to_id_convert(raw_name, dvhc_json):
    """
    Convert region (Tỉnh, thành phố ~ level 1) to id (string)
    """
    new_name = __get_place_name(raw_name)
    if pd.isna(raw_name):
        return pd.NA

    for l1_key, l1_val in dvhc_json.items():
        if new_name == l1_val["alias"]:
            return l1_key
    return pd.NA


def __area_to_id_convert(region_id, raw_name, dvhc_json):
    """
    Convert area (Quận, Huyện, thị xã ~ level 2) to id (string)
    """
    new_name = __get_place_name(raw_name)
    if pd.isna(raw_name):
        return pd.NA

    for l2_key, l2_val in dvhc_json[region_id]["level2s"].items():
        if new_name == l2_val["alias"]:
            return l2_key
    return pd.NA


def __ward_to_id_convert(region_id, area_id, raw_name, dvhc_json):
    """
    Convert ward (Phường, xã, thị trấn ~ level 3) to id (string)
    """
    new_name = __get_place_name(__extract_ward(raw_name))
    if pd.isna(new_name):
        return pd.NA

    for l3_key, l3_val in dvhc_json[region_id]["level2s"][area_id]["level3s"].items():
        if new_name == l3_val["alias"]:
            return l3_key
    return pd.NA


def address_convert_all(df: pd.DataFrame):
    """Convert Region, area, ward to id"""

    def convert_row(row, dvhc_json):
        region_id = __region_to_id_convert(row["City"], dvhc_json)
        if pd.isna(region_id):
            return pd.Series({"City": pd.NA, "District": pd.NA, "Ward": pd.NA})

        area_id = __area_to_id_convert(region_id, row["District"], dvhc_json)
        if pd.isna(area_id):
            return pd.Series({"City": region_id, "District": pd.NA, "Ward": pd.NA})

        ward_id = __ward_to_id_convert(region_id, area_id, row["DiaChi"], dvhc_json)
        return pd.Series({"City": region_id, "District": area_id, "Ward": ward_id})

    def convert_row_hybrid(row):
        res = convert_row(row, _dvhc_json_2020)
        if res.isna().any():
            # Retry with another version
            res = convert_row(row, _dvhc_json_2024)
        return res

    if "Ward" not in df:
        df["Ward"] = pd.NA

    df[["City", "District", "Ward"]] = df.apply(convert_row_hybrid, axis=1).astype(
        pd.Int32Dtype()
    )


def region_deconvert(id):
    if pd.isna(id):
        return pd.NA
    id = str(int(float(id)))
    if id in _dvhc_json_2020.keys():
        return _dvhc_json_2020[id]["name"]
    if id in _dvhc_json_2024.keys():
        return _dvhc_json_2024[id]["name"]
    return pd.NA


def area_deconvert(reg_id, are_id):
    if pd.isna([reg_id, are_id]).any():
        return pd.NA
    reg_id = str(int(float(reg_id)))
    are_id = str(int(float(are_id)))
    if are_id in _dvhc_json_2020[reg_id]["level2s"].keys():
        return _dvhc_json_2020[reg_id]["level2s"][are_id]["name"]
    if are_id in _dvhc_json_2024[reg_id]["level2s"].keys():
        return _dvhc_json_2024[reg_id]["level2s"][are_id]["name"]
    return pd.NA


def ward_deconvert(reg_id, are_id, ward_id):
    if pd.isna([reg_id, are_id, ward_id]).any():
        return pd.NA
    reg_id = str(int(float(reg_id)))
    are_id = str(int(float(are_id)))
    ward_id = str(int(float(ward_id)))
    if ward_id in _dvhc_json_2020[reg_id]["level2s"][are_id]["level3s"].keys():
        return _dvhc_json_2020[reg_id]["level2s"][are_id]["level3s"][ward_id]["name"]
    if ward_id in _dvhc_json_2024[reg_id]["level2s"][are_id]["level3s"].keys():
        return _dvhc_json_2024[reg_id]["level2s"][are_id]["level3s"][ward_id]["name"]
    return pd.NA


def get_all_regions():
    return [
        {"label": val["name"], "value": key} for key, val in _dvhc_json_2020.items()
    ]


def get_all_areas(reg_id):
    if pd.isna(reg_id):
        return pd.NA
    return [
        {"label": (val["type"] + " " + val["name"]), "value": key}
        for key, val in _dvhc_json_2020[reg_id]["level2s"].items()
    ]


def get_all_wards(reg_id, are_id):
    if pd.isna([reg_id, are_id]).any():
        return pd.NA
    return [
        {"label": (val["type"] + " " + val["name"]), "value": key}
        for key, val in _dvhc_json_2020[reg_id]["level2s"][are_id]["level3s"].items()
    ]


#################################################### Load dvhc ####################################################
# Get the absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = (
    "/".join(i for i in current_dir.split("\\")[:-3]) + "/data/donvihanhchinhvn/"
)


def load_dvhc_file(file_name) -> dict:
    with open(json_path + file_name, "r", encoding="utf8") as dvhc_file:
        dvhc_json = json.load(dvhc_file)
    return dvhc_json


_dvhc_json_2024 = load_dvhc_file("dvhcvn_2024.json")
_dvhc_json_2020 = load_dvhc_file("dvhcvn_2020.json")
