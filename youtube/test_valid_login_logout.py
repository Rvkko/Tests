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
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    driver.get('https://www.youtube.com/')

    sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620']")))
    sign_in.click()

    email = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    email.send_keys(test_data['email'])

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")))
    next_button.click()

    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys(['Admin123!'])

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")))
    next_button.click()

    dropdown =wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@src='https://yt3.ggpht.com/yti/ANjgQV9Zp79uBmsFWkgH6VdnUpEoJRXYWgqUGtrpvxAoE3o=s88-c-k-c0x00ffffff-no-rj-mo']")))
    dropdown.click()

    logout_button =wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/logout']")))
    logout_button.click()

    WebDriverWait(driver, 5).until(EC.url_contains('https://www.youtube.com/'))
    actual_url = driver.current_url
    assert actual_url.startswith('https://www.youtube.com/')