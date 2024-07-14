# get id san pham: https://gateway.chotot.com/v2/public/deeplink-resolver?siteId=3&url=%2F<full link>
# get detail: https://gateway.chotot.com/v2/public/ad-listing/<id san pham>?adview_position=true&tm=treatment2

# ad: price, latitude, longitude, category_name
# parameters:
# 	ward: Phường, thị xã, thị trấn
# 	property_status: Tình trạng bất động sản
# 	price_m2: giá/m2
# 	rooms: phòng ngủ
# 	toilets: số toilet
# 	apartment_type: Loại hình căn hộ
# 	property_legal_document: Giấy tờ pháp lý
# 	area: Quận, Huyện
# 	region: Tỉnh, thành phố
# 	address: Địa chỉ
# 	furnishing_sell: Tình trạng nội thất
# 	size: diện tích
# 	house_type: Loại hình nhà
# 	floors: Tổng số tầng
# 	pty_characteristics: Đặc điểm nhà/đất
# 	direction: Hướng cửa chính

import json
from selenium import webdriver
from bs4 import BeautifulSoup
from unidecode import unidecode

import custom_modules.common as common


def extract_property_urls_single_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://www.nhatot.com/"
    property_urls = [
        base_url + element.get("href")
        for element in soup.select("a.AdItem_adItem__gDDQT")
    ]
    return property_urls


driver = common.createChromeDriver()
html = driver.get("https://www.nhatot.com/mua-ban-can-ho-chung-cu?page=2")
print(extract_property_urls_single_page(html.page_source))
driver.close()
driver.quit()


def process_single_property(property_url, chrome_driver):
    chrome_driver.get(property_url)
    html_content = chrome_driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    property_data = {}

    # Find property info

    # Find property city & District & Ward

    # Find property map coordinates

    return property_data
