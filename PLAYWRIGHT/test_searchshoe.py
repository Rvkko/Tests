import pytest
import os
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    yield driver, wait
    driver.quit()

@pytest.fixture
def nike_data():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_directory, 'nike_data.json')
    with open(json_file_path) as f:
        data = json.load(f)
    return data

def test_navigation(driver, nike_data):
    driver, wait = driver
    driver.get('https://www.nike.com/')

    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    search.send_keys(nike_data['shoe'])
    search.send_keys(Keys.ENTER)

    select_shoe = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@href='https://www.nike.com/t/air-jordan-11-retro-legend-blue-big-kids-shoes-KK99vE/378038-104']")))
    select_shoe.click()

    size_selcetion = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='grid-selector-input-8.5']")))
    size_selcetion.click()

    add_to_bag = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='add-to-bag']")))
    add_to_bag.click()

    checkout = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
    checkout.click()

    customer_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.nike.com/cart']")))
    customer_cart.click()