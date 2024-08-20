import numpy as np
import pandas as pd
from unidecode import unidecode


def __legalty_convert(s) -> int:
    """
    # Convert property legal document to integer
    Không sổ : 0
    Đã có sổ: 1
    Đang chờ sổ: 2
    Sổ chung | công chứng vi bằng: 3
    viết tay: 4
    """
    if pd.isna(s):
        return np.nan

    s = unidecode(s.lower().replace(" ", ""))

    # Đang chờ sổ: 2
    trait = [
        "dangcho",
        "dangdoi",
        "chocap",
        "choso",
        "chuanbi",
        "dangra",
        "danglam",
        "dangnop",
        "cholam",
        "doilam",
    ]
    if any(i in s for i in trait):
        return 2

    # Sổ chung | công chứng vi bằng : 3
    trait = [
        "sochung",
        "vibang",
        "vb",
        "dongsohuu",
        "shc",
        "sdc",
        "sodochung",
        "sohongchung",
    ]
    exc = ["shcc", "sdcc", "chinhchu"]
    if any(i in s for i in trait) and not any(i in s for i in exc):
        return 3

    # Đã có sổ: 1
    trait = [
        "coso",
        "sodo",
        "sd",
        "biado",
        "quyensudungdat",
        "giayphepxaydung",
        "gpxd",
        "sohong",
        "sh",
        "biahong",
        "sosan",
        "sanso",
        "cosan",
        "sodep",
        "socongchung",
        "vuongdep",
        "vuongvan",
        "sovuong",
        "sodat",
        "catket",
        "sorieng",
        "sohongrieng",
        "sonet",
        "chinhchu",
        "hoancong",
        "laudai",
        "thocu",
        "daydu",
        "sangten",
        "vinhvien",
        "hople",
        "hopphap",
        "phaplychuan",
        "phaplysach",
        "minhbach",
        "rorang",
        "sodenganhang",
        "giaychungnhan",
        "quyensohuunha",
    ]
    exc = ["chuaco", "chuaso", "khongso", "seraso", "secapso"]
    if any(i in s for i in trait) and not any(i in s for i in exc):
        return 1
    if len(s) <= 3 and s == "so":
        return 1

    # viết tay: 4
    trait = ["viettay", "giaytay", "hopdong", "hdmb", "thoathuan", "hdm"]
    exc = []
    if any(i in s for i in trait) and not any(i in s for i in exc):
        return 4

    return 0


def __furnishment_convert(s) -> int:
    """
    # Convert furnishment to integer
    Không: 0
    Cao cấp: 1
    Đầy đủ | hoàn thiện: 2
    Cơ bản: 3
    """
    if pd.isna(s):
        return np.nan

    s = unidecode(s.lower().replace(" ", ""))

    trait = [
        "caocap",
        "sangtrong",
        "xin",
        "5*",
        "dangcap",
        "chuyennghiep",
        "quy",
        "vip",
        "namsao",
        "chauau",
        "nhap",
        "sangtrong",
        "datvang",
        "tienty",
        "dattien",
        "lim",
    ]
    # Cao cấp: 1
    if any(i in s for i in trait):
        return 1

    # Đầy đủ | hoàn thiện: 2
    trait = [
        "daydu",
        "hoanthien",
        "du",
        "full",
        "toanbo",
        "hiendai",
        "dep",
        "san",
        "delai",
        "tang",
        "chatluongcao",
    ]
    if any(i in s for i in trait):
        return 2

    # Cơ bản: 3
    trait = [
        "coban",
        "binhdan",
        "cu",
        "conoithat",
        "condep",
        "chuan",
        "maylanh",
        "dieuhoa",
        "tulanh",
        "giuong",
        "tivi",
        "tv",
        "sofa",
        "sopha",
        "nhumoi",
        "nonglanh",
        "noithatdinhtuong",
        "moitinh",
        "tot",
        "lientuong",
        "nhuhinh",
        "trangbi",
        "dinhtuong",
    ]
    if any(i in s for i in trait):
        return 3

    return 0


def __direction_convert(s) -> int:
    """
    # Convert direction to integer
    Đông: 1
    Tây: 2
    Nam: 3
    Bắc: 4
    Đông - Bắc: 5
    Đông - Nam: 6
    Tây - Bắc: 7
    Tây - Nam: 8
    """
    if pd.isna(s):
        return np.nan
    if "Đông" == s:
        return 1
    if "Tây" == s:
        return 2
    if "Nam" == s:
        return 3
    if "Bắc" == s:
        return 4
    if "Đông - Bắc" == s:
        return 5
    if "Đông - Nam" == s:
        return 6
    if "Tây - Bắc" == s:
        return 7
    if "Tây - Nam" == s:
        return 8


def legal_document_deconvert(num) -> str:
    """
    # Deconvert property legal document to string
    0: Uncertified
    1: Certified
    2: Awaiting certification
    3: Shared/notarized certification
    4: Handwritten document
    """
    if pd.isna(num):
        return np.nan
    if num == 0:
        return "Uncertified"
    if num == 1:
        return "Certified"
    if num == 2:
        return "Awaiting certification"
    if num == 3:
        return "Shared/notarized certification"
    if num == 4:
        return "Handwritten document"


def furnishment_deconvert(num) -> str:
    """
    # Deconvert furnishment to string
    0: Unfurnished
    1: Expensively furnished
    2: Well furnished
    3: Simply furnished
    """
    if pd.isna(num):
        return np.nan
    if num == 0:
        return "Unfurnished"
    if num == 1:
        return "Expensively furnished"
    if num == 2:
        return "Fully furnished"
    if num == 3:
        return "Simply furnished"


def direction_deconvert(num) -> str:
    """
    # Deconvert direction to string
    East: 1
    West: 2
    South: 3
    North: 4
    North - East: 5
    South - East: 6
    North - West: 7
    South - West: 8
    """
    if pd.isna(num):
        return np.nan
    if num == 1:
        return "East"
    if num == 2:
        return "West"
    if num == 3:
        return "South"
    if num == 4:
        return "North"
    if num == 5:
        return "North - East"
    if num == 6:
        return "South - East"
    if num == 7:
        return "North - West"
    if num == 8:
        return "South - West"


def legalty_convert_all(df: pd.DataFrame):
    df["PhapLy"] = df["PhapLy"].apply(__legalty_convert).astype(pd.Int8Dtype())


def furnishment_convert_all(df: pd.DataFrame):
    df["NoiThat"] = df["NoiThat"].apply(__furnishment_convert).astype(pd.Int8Dtype())


def direction_convert_all(df: pd.DataFrame, col_name):
    df[col_name] = df[col_name].apply(__direction_convert).astype(pd.Int8Dtype())


def get_all_legal_status():
    return [
        {"label": "Uncertified", "value": 0},
        {"label": "Certified", "value": 1},
        {"label": "Certifying", "value": 2},
        {"label": "Shared / notarized document", "value": 3},
        {"label": "Hand-written contract", "value": 4},
    ]


def get_all_furnishment():
    return [
        {"label": "Nothing", "value": 0},
        {"label": "Expensive", "value": 1},
        {"label": "Full", "value": 2},
        {"label": "Basic", "value": 3},
    ]


def get_all_directions():
    return [
        {"label": "East", "value": 1},
        {"label": "West", "value": 2},
        {"label": "South", "value": 3},
        {"label": "North", "value": 4},
        {"label": "North - East", "value": 5},
        {"label": "South - East", "value": 6},
        {"label": "North - West", "value": 7},
        {"label": "South - West", "value": 8},
    ]
