import numpy as np
import pandas as pd


# Xử lý diện tích
def area_transform(df):
    df["DienTich"] = (
        df["DienTich"]
        .str.replace(" m²", "")
        .str.replace(".", "")
        .str.replace(",", ".")
        .str.strip()
    )
    df["DienTich"] = pd.to_numeric(
        df["DienTich"], errors="coerce"
    )  # Chuyển đổi sang float và tạo NaN cho giá trị không hợp lệ


# Hàm chuyển đổi đơn vị giá -> đồng
def __price_transform(price, area):
    if isinstance(price, (float, int)):
        return price

    price = str(price)

    per_m2 = False
    if "m²" in price:
        price = price.replace("/m²", "")
        per_m2 = True

    if "nghìn" in price:
        price_value = 1_000 * np.float64(
            price.replace(" nghìn", "").replace(".", "").replace(",", ".")
        )
        return (price_value * area) if per_m2 else price_value
    if "triệu" in price:
        price_value = 1_000_000 * np.float64(
            price.replace(" triệu", "").replace(".", "").replace(",", ".")
        )
        return (price_value * area) if per_m2 else price_value
    if "tỷ" in price:
        price_value = 1_000_000_000 * np.float64(
            price.replace(" tỷ", "").replace(".", "").replace(",", ".")
        )
        return (price_value * area) if per_m2 else price_value

    return pd.NA


# Xử lý giá
def price_convert(df):
    df["MucGia"] = df.apply(
        lambda row: __price_transform(row["MucGia"], row["DienTich"]), axis=1
    )


# Xử lý diện tích mặt tiền
def facade_transform(df):
    df["MatTien"] = pd.to_numeric(
        df["MatTien"].str.replace(" m", "").str.replace(",", ".").str.strip()
    )


# Xử lý diện tích đường vào
def way_transform(df):
    df["DuongVao"] = pd.to_numeric(
        df["DuongVao"].str.replace(" m", "").str.replace(",", ".").str.strip()
    )


# Xử lý diện tích số phòng ngủ
def bedrooms_transform(df):
    df["SoPhongNgu"] = pd.to_numeric(
        df["SoPhongNgu"].str.replace(" phòng", "").str.strip(), downcast="integer"
    )


# Xử lý số phòng Toilet
def toilets_transform(df):
    df["SoToilet"] = pd.to_numeric(
        df["SoToilet"].str.replace(" phòng", "").str.strip(), downcast="integer"
    )


# Xử lý số tầng
def floor_transform(df):
    df["SoTang"] = pd.to_numeric(
        df["SoTang"].str.replace(" tầng", "").str.strip(), downcast="integer"
    )


# Main Preprocess_Digit
def numbers_convert(df: pd.DataFrame):
    area_transform(df)
    price_convert(df)
    facade_transform(df)
    way_transform(df)
    bedrooms_transform(df)
    toilets_transform(df)
    floor_transform(df)
