from selenium import webdriver
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode

import json
import re
import logging
import os
import random


###################### Utility Function ######################
def extract_page_in_url(url: str):
    return url.rsplit("/", 1)[-1]


def get_current_time_str():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M")
    return formatted_datetime


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


def createChromeDriver(num_chrome) -> list[webdriver.Chrome]:
    # Configure webdriver to disable images and js
    options = webdriver.ChromeOptions()
    chrome_prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "images": 2,
            "javascript": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
    }
    options.experimental_options["prefs"] = chrome_prefs
    # options.add_argument("--headless=new")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")

    chrome_drivers = []
    for _ in range(num_chrome):
        driver = webdriver.Chrome(options=options)
        chrome_drivers.append(driver)
    return chrome_drivers


def extract_property_urls_single_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://batdongsan.com.vn"
    property_urls = [
        base_url + element.get("href")
        for element in soup.select(".js__product-link-for-product-id")
    ]
    return property_urls


###################### Multi-threaded Selenium Scrapping Function ######################
def process_single_property(property_url, chrome_driver: webdriver.Chrome):
    # logging.info(property_url)
    chrome_driver.get(property_url)
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


def process_single_page(
    page_url, chrome_driver: webdriver.Chrome, limit_each_page, max_retry=1
):
    logging.info(f"The process's scrapping {page_url}...")
    properties = []
    for attempt in range(max_retry + 1):
        try:
            chrome_driver.get(page_url)

            # Check for Cloudflare bot detection
            if "Cloudflare" in chrome_driver.page_source:
                raise Exception("Cloudflare detected in the page source")

            # Scrapping data for each property
            html_content = chrome_driver.page_source
            property_urls = extract_property_urls_single_page(html_content)
            for idx, property_url in zip(range(limit_each_page), property_urls):
                properties.append(process_single_property(property_url, chrome_driver))
                sleep(random.randint(1, 3))

            # Write to local
            file_name = f"../../data/{get_current_time_str()}_{extract_page_in_url(page_url)}.json"
            with open(file_name, "w", encoding="utf-8") as json_file:
                json.dump(properties, json_file, indent=1)

            logging.info(f"Scrapping {page_url} done.")
            return properties
        except Exception as e:
            logging.info(f"Attempt {attempt + 1}: Error - {e}, try again in 5s")
            sleep(5)

    logging.info(f"All attempts failed. Returning None for {page_url}")
    return []


def process_multiple_pages(id_range, chrome_driver, store, limit_each_page):
    if store is None:
        store = []
    for url in id_range:
        store.append(process_single_page(url, chrome_driver, limit_each_page))
    return store


def threaded_selenium_scrapping(nthreads, id_range, limit_each_page):
    store = []
    threads = []
    chrome_drivers = createChromeDriver(nthreads)
    for idx, chrome_driver in enumerate(chrome_drivers):
        ids = id_range[idx::nthreads]
        logging.info(ids)
        t = Thread(
            target=process_multiple_pages,
            args=(ids, chrome_driver, store, limit_each_page),
        )
        threads.append(t)

    # start the threads
    [t.start() for t in threads]
    # wait for the threads to finish
    [t.join() for t in threads]

    # with open(f"reconciled_data/{get_current_time_str()}_reconciled_properies.json", 'w',encoding='utf-8') as json_file:
    #     json.dump(store, json_file, ensure_ascii=False, indent=4)

    for cd in chrome_drivers:
        cd.quit()
