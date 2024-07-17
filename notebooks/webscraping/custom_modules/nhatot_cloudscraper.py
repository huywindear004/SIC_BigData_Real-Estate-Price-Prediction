# get id san pham: https://gateway.chotot.com/v2/public/deeplink-resolver?siteId=3&url=%2F<full link>
# get detail: https://gateway.chotot.com/v2/public/ad-listing/<id san pham>?adview_position=true&tm=treatment2

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
#       1: đã có sổ | 2: đang chờ sổ | 3: không có sổ | 4: sổ chung/công chứng vi bằng | 5: giấy tờ viết tay
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
#   
#   
#   
#   
#   
#   
#   
#   
#   
# parameters:

import cloudscraper
from bs4 import BeautifulSoup
from unidecode import unidecode

import json

import common as common


def extract_property_urls_single_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://www.nhatot.com"
    property_urls = [
        base_url + element.get("href")
        for element in soup.select("a.AdItem_adItem__gDDQT")
    ]
    return property_urls


scraper = cloudscraper.create_scraper(
    delay=10, browser={"browser": "chrome", "platform": "windows", "mobile": False}
)
html = scraper.get("https://www.nhatot.com/mua-ban-can-ho-chung-cu?page=2").text
with open("cc.html", "w", encoding="utf-8") as file:
    file.write(str(extract_property_urls_single_page(html)))


def process_single_property(property_url, chrome_driver):
    chrome_driver.get(property_url)
    html_content = chrome_driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    property_data = {}

    # Find property info

    # Find property city & District & Ward

    # Find property map coordinates

    return property_data
