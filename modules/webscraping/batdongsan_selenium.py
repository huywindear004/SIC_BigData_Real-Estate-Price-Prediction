from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from unidecode import unidecode

import re
import random
from threading import Thread
from time import sleep

import common as common


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


def extract_property_urls_single_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://batdongsan.com.vn"
    property_urls = [
        base_url + element.get("href")
        for element in soup.select(".js__product-link-for-product-id")
    ]
    return property_urls


def process_single_property(property_url, chrome_driver: webdriver.Chrome):
    wait = WebDriverWait(chrome_driver, 5)
    chrome_driver.get(property_url)
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".re__section.re__pr-map.js__section.js__li-other")
        )
    )
    chrome_driver.execute_script("window.stop();")

    html_content = chrome_driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    property_data = {}

    # Find property info
    elements = soup.find_all("div", class_="re__pr-specs-content-item")
    for item in elements:
        key = item.find("span", class_="re__pr-specs-content-item-title").text
        value = item.find("span", class_="re__pr-specs-content-item-value").text
        property_data[unidecode(key.title().replace(" ", ""))] = value

        # Find property address
        address = soup.find(
            "span", class_="re__pr-short-description js__pr-address"
        ).text
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


def process_single_page(page_url, driver, max_retry=0):
    properties = []
    for attempt in range(max_retry + 1):
        try:
            print("Processing:", page_url)
            wait = WebDriverWait(driver, 30)
            driver.get(page_url)

            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".js__product-link-for-product-id")
                )
            )
            driver.execute_script("window.stop();")

            # Check for Cloudflare bot detection
            if "Cloudflare" in driver.page_source:
                raise Exception("Cloudflare detected in the page source")

            # Scrapping data for each property
            html_content = driver.page_source
            property_urls = extract_property_urls_single_page(html_content)
            for property_url in property_urls:
                properties.append(process_single_property(property_url, driver))
                # sleep(random.randint(1, 3))
                sleep(1)

            return properties
        except Exception:
            if attempt < max_retry:
                sleep(5)
    raise Exception("Couldn't crawl data from", page_url)


def process_multiple_pages(base_url, page_ids, driver, store, filter=""):
    if store is None:
        store = []

    for idx in page_ids:
        store += process_single_page(f"{base_url}{idx}{filter}", driver)

    return store


def multi_threaded_scraping(
    num_threads, file_out_path, base_url, start, end, typeOfProperty, filter=""
):
    threads = []
    store = []

    page_range = list(range(start, end + 1))
    drivers = [common.createChromeDriver() for _ in range(num_threads)]

    # Split the page_range into parts
    for idx, driver in enumerate(drivers):
        ids = page_range[idx::num_threads]
        thread = Thread(
            target=process_multiple_pages, args=(base_url, ids, driver, store, filter)
        )
        threads.append(thread)

    try:
        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for the threads to finish
        for thread in threads:
            thread.join()
    except:
        pass
    finally:
        # Quit all the drivers
        for driver in drivers:
            driver.quit()
        # Write to file
        common.write_json_file(file_out_path, store, start, end, typeOfProperty)
