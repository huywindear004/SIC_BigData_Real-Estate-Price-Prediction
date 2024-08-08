import cloudscraper
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from time import sleep
import random
from datetime import datetime


import common as common


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
        raise Exception(
            f"Couldn't get {property_url}. Status code: {response.status_code}"
        )

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
    address = soup.select("span.re__pr-short-description.js__pr-address").text
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
        raise Exception(f"Couldn't get {page_url}. Status code: {response.status_code}")
    properties = []
    prop_urls = extract_property_urls(response.text)
    for prop_url in prop_urls:
        properties.append(process_single_property(prop_url, scraper))
        sleep(random.randint(1, 3))
    return properties


def process_multiple_pages(
    fileOutPath, base_url, start, end, typeOfProperty="batdongsan", retryEachPage=0
):
    scraper = cloudscraper.create_scraper(
        delay=10, browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    temp = []
    prev = start
    i = start
    try:
        for i in range(start, end + 1):
            # Try
            for tryCount in range(retryEachPage + 1):
                try:
                    temp += process_single_page(base_url + str(i), scraper)
                    break
                except Exception as e:
                    if tryCount < retryEachPage:
                        print("Wait for retry")
                        sleep(100)
                    else:
                        raise e
            # Each file contains 100 x 20 collections
            if i % 100 == 0:
                # Write to local
                common.write_json_file(fileOutPath, temp, prev, i, typeOfProperty)
                prev = i + 1
                temp.clear()
    except Exception as e:
        print(f"Error: {e.with_traceback()}")
        i -= 1
    finally:
        if len(temp) > 0:
            common.write_json_file(fileOutPath, temp, prev, i, typeOfProperty)
