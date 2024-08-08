import json
from selenium import webdriver
from datetime import datetime
import os


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36",
]


def write_json_file(path, data, start, end, typeOfProp):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(
        path
        + f"{typeOfProp}-dataset_page-{start:0>5}~{end:0>5}_{get_current_time_str()}.json",
        "w",
        encoding="utf-8",
    ) as fileOut:
        json.dump(data, fileOut, indent=1)


def get_current_time_str():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y")
    return formatted_datetime


def createChromeDriver() -> webdriver.Chrome:
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
    options.add_argument("--headless=new")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    )
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    # Stop when html is loaded
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    return driver
