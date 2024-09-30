import json
import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    yield driver, wait
    driver.quit()

@pytest.fixture
def test_data():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_directory, 'test_data.json')
    with open(json_file_path) as f:
        data = json.load(f)
    return data

def test_login_logout(driver, test_data):
    driver, wait = driver
    driver.get('https://weather.com/')

    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='LocationSearch_input']")))
    search.send_keys(test_data['location'])

    navigate = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='LocationSearch_listbox-a2d94c2f7f4b4f711bf9befdfb29bbb34c2472136ba4d5c20331517c13305ba6']")))
    navigate.click()

    WebDriverWait(driver, 5).until(EC.url_contains('https://weather.com/'))
    actual_url = driver.current_url
    assert actual_url.startswith('https://weather.com/')