import time
import os
from selenium2.utils.helpers import extract_domain

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium2.constants import CHROME_DRIVER_PATH

# Get the current directory and set the ChromeDriver path
current_dir = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(current_dir, CHROME_DRIVER_PATH)

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
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu')
    
    # Use this when testing on windows
    service = Service(f"{chrome_driver_path}")
    try:
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(options=options)
    
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
    
        return page_html
    except Exception as e:
        print(f"An error occurred during automation: {e}")
        return None
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    