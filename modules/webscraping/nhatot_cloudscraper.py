# get detail: https://gateway.chotot.com/v2/public/ad-listing/<id san pham>?adview_position=true&tm=treatment2

# Get siêu ung thư:
# https://gateway.chotot.com/v1/public/ad-listing?cg=1040&o=0&page=1&st=s,k&limit=100&key_parameter_included=true

# cg: loại sản phẩm
#   căn hộ: 1010
#   nhà ở: 1020
#   văn phòng, mặt bằng kinh doanh: 1030
#   đất: 1040

# có thể thêm 'region_v2'(id của tỉnh thành) và 'area_v2'(id của quận huyện) để lọc

# Các thuộc tính cần lấy:
#       address: Địa chỉ
#       street_number:
#       street_name: tên đường
#       ward: Phường, thị xã, thị trấn
#       area: Quận, Huyện
#       region: Tỉnh, thành phố

#       property_status: Tình trạng bất động sản
#       property_legal_document: Giấy tờ pháp lý
#       price_m2: giá/m2
#       rooms: phòng ngủ
#       toilets: số toilet
#       furnishing_sell: Tình trạng nội thất
#       floors: Tổng số tầng

#       pty_characteristics: Đặc điểm nhà/đất
#       direction: Hướng cửa chính
#       apartment_type: Loại hình căn hộ
#       house_type: Loại hình nhà

#       latitude: Vĩ độ
#       longitude: Kinh độ

# ad:
#   price: Giá (tổng, đồng)
#   size: Diện tích (m2)
#   long-lat: kinh-vĩ độ
#   property_legal_document: Giấy tờ pháp lý
#       1: đã có sổ | 2: đang chờ sổ | 4: không có sổ | 5: sổ chung/công chứng vi bằng | 6: giấy tờ viết tay
#   pty_characteristics: Đặc điểm nhà đất
#       1: Mat tien, 2: Hem xe hoi, 3: Nở hậu, 4: Chưa có thổ cư, 5: thổ cư 1 phần, 6: thổ cư toàn bộ, 7: Không có thổ cư
#   land_type: loại hình đất
#       1: đất thổ cư | 2: đất nền dự án | 3: đất công nghiệp | 4: đất nông nghiệp
#   width: rộng(m)
#   length: dài(m)
#   street_number (có thể có): số nhà trên đường
#   street_name (có thể có): tên đường
#   category_name: thể loại bds
#   area_name: Quận, Huyện
#   region_name: Tỉnh, thành phố
#   ward_name:

import requests
import time
import numpy as np
import random

import common


def process_json_data(json_data):
    res = []
    for i in json_data["ads"]:
        item = {
            "Street": i.get("street_name"),
            "Ward": i.get("ward_name"),
            "Area": i.get("area_name"),
            "Region": i.get("region_name"),
            "Latitude": i.get("latitude"),
            "Longitude": i.get("longitude"),
            "Price": i.get("price"),
            "PriceMillionPerM2": i.get("price_million_per_m2"),
            "Size": i.get("size"),
            "Characteristics": i.get("pty_characteristics"),
            "LandType": i.get("land_type"),
            "Width": i.get("width"),
            "Length": i.get("length"),
            "direction": i.get("direction"),
        }
        # Trên web:
        #     1: đã có sổ | 2: đang chờ sổ | 4: không có sổ | 5: sổ chung/công chứng vi bằng | 6: giấy tờ viết tay
        # Quy ước:
        #     Không sổ : 0 |Đã có sổ: 1 |Đang chờ sổ: 2 |Sổ chung/công chứng vi bằng: 3 |viết tay: 4
        legalty = i.get("property_legal_document")
        if legalty == 4:
            legalty = 0
        elif legalty == 5:
            legalty = 3
        elif legalty == 6:
            legalty = 4
        item["Legalty"] = legalty

        res.append(item)
    return res


def run(path, cate_id, start, end, limit_each_page, try_limit=0, type="batdongsan"):
    page = start
    start -= 1
    try_count = 0
    o = start * limit_each_page
    res = []
    while page <= end:
        try:
            url = f"https://gateway.chotot.com/v1/public/ad-listing?cg={cate_id}&o={o}&st=s,k&limit={limit_each_page}&key_parameter_included=true"
            headers = {"User-Agent": random.choice(common.user_agents)}
            r = requests.get(headers=headers, url=url)
            if r.status_code != 200:
                raise Exception

            res += process_json_data(r.json())

        except:
            print("error")
            if try_count < try_limit:
                try_count += 1
                time.sleep(random.random(20, 60))
                continue
            else:
                pass
        finally:
            pass

        time.sleep(np.random.choice([x / 10 for x in range(3, 12)]))
        page += 1
        o += limit_each_page
    common.write_json_file(path, res, start, end, type)
