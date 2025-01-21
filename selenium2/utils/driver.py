import time
import os
from selenium2.utils.helpers import clean_form_labels, extract_domain

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
        find_and_click_easy_apply(driver) 
        answer_form_questions(driver)
        # submit_form(driver)
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
    
def find_and_click_easy_apply(driver):
    try:
        easy_apply_button = driver.find_elements("xpath", "//button")
        print(easy_apply_button)
        for button in easy_apply_button:
            try:
                button_text = button.get_attribute("outerHTML")
                print(button_text)
                
                if "Easy Apply" in button_text:
                    button.click()
                    print(f"{button}. Button found")
                    break
                else:
                    print(f"{button}. Other buttons")
            except Exception as e:
                print(f"Error processing a button: {e}")
        time.sleep(3)
    except Exception as e:
        print(f"An error occurred while interacting with the Easy Apply form: {e}")
        return None

def answer_form_questions(driver):
    try:
        questions_elements = driver.find_elements("xpath", "//form//label")  # Adjust XPath as needed
        questions = [question.get_attribute("outerHTML") for question in questions_elements if question.get_attribute("outerHTML").strip() != ""]
        
        print("Form Questions:", clean_form_labels(questions))
        return questions
    except Exception as e:
        print(f"An error occurred while answering form questions: {e}")
        return None