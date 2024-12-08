import time
import os
from utils.helpers import extract_domain

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from constants import CHROME_DRIVER_PATH

def automate(url, path, cookie_string):
    DOMAIN = extract_domain(url)
    cookies = []
    for item in cookie_string.split(";"):
        name, value = item.strip().split("=", 1)
        cookies.append({
            "name": name,
            "value": value,
            "domain": DOMAIN,
            "path": "/",
            "secure": False,
            "httpOnly": False,
            "expiry": None
        })
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-minimized")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Use this when testing on windows
    # service = Service(f"{current_directory}/{CHROME_DRIVER_PATH}")
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    
    for cookie in cookies:
            cookie.pop('expiry', None)
            driver.add_cookie(cookie)
    time.sleep(5)
    driver.refresh()
    driver.implicitly_wait(10)
    
    driver.get(f"{url}{path}")
    
    # Add automation for easy apply
    page_html = driver.page_source
    
    # time.sleep(10)
    driver.quit()
    
    return page_html