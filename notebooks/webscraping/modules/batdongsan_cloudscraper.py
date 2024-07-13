import cloudscraper
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from time import sleep
import random
import json
from datetime import datetime


def get_current_time_str():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M")
    return formatted_datetime


def extract_page_in_url(url: str):
    return url.rsplit("/", 1)[-1]


def extract_coordinates(html_content):
    # Define a regular expression pattern to extract coordinates
    pattern = r"place\?q=([-+]?\d*\.\d+),([-+]?\d*\.\d+)"

    # Use re.search to find the first match in the HTML content
    match = re.search(pattern, html_content)

    # Check if a match is found
    if match:
        # Extract latitude and longitude from the matched groups
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return [latitude, longitude]
    else:
        return [None, None]


def extract_property_urls(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://batdongsan.com.vn"
    property_urls = [
        base_url + element.get("href")
        for element in soup.select(".js__product-link-for-product-id")
    ]
    return property_urls


def process_single_property(property_url, scraper: cloudscraper.CloudScraper):
    response = scraper.get(property_url)

    if response.status_code != 200:
        return

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    property_data = {}

    # Find property info
    elements = soup.find_all("div", class_="re__pr-specs-content-item")
    for item in elements:
        key = item.find("span", class_="re__pr-specs-content-item-title").text
        value = item.find("span", class_="re__pr-specs-content-item-value").text
        property_data[unidecode(key.title().replace(" ", ""))] = value

    # Find property address
    address = soup.find("span", class_="re__pr-short-description js__pr-address").text
    property_data["DiaChi"] = address

    # Find property city & District & Ward
    breadCrumb_addr = soup.select(
        "div.re__breadcrumb.js__breadcrumb.js__ob-breadcrumb .re__link-se"
    )
    property_data["City"] = breadCrumb_addr[1].text
    property_data["District"] = breadCrumb_addr[2].text

    # Find property map coordinates
    map_coor = soup.find(
        "div", class_="re__section re__pr-map js__section js__li-other"
    )
    map_coor = extract_coordinates(str(map_coor))
    property_data["Lat"] = map_coor[0]
    property_data["Long"] = map_coor[1]

    return property_data


def process_single_page(page_url, scraper):
    print("Processing:", page_url)
    response = scraper.get(page_url)
    if response.status_code != 200:
        return
    properties = []
    prop_urls = extract_property_urls(response.text)
    for prop_url in prop_urls:
        properties.append(process_single_property(prop_url, scraper))
        sleep(random.randint(1, 3))
    return properties


def process_multiple_pages(base_url, start, end, typeOfProperty="batdongsan"):
    scraper = cloudscraper.create_scraper(
        delay=10, browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    temp = []
    prev = start
    for i in range(start, end + 1):
        temp += process_single_page(base_url + str(i), scraper)

        # Each file contains 20 x 20 collections
        if i % 20 == 0:
            temp.clear()
            # Write to local
            file_name = f"../../data/{typeOfProperty}_page-{prev}~{i}_{get_current_time_str()}.json"
            with open(file_name, "w", encoding="utf-8") as json_file:
                json.dump(temp, json_file, indent=1)
            prev = i + 1

    if len(temp) > 0:
        file_name = (
            f"../../data/{typeOfProperty}_page-{prev}~{i}_{get_current_time_str()}.json"
        )
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(temp, json_file, indent=1)
