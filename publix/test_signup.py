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
    wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    driver.get('https://www.publix.com/')

    sign_up_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-label="Sign up" and @role="button"]')))
    sign_up_button.click()

    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_FirstName10']")))
    first_name.send_keys(['Derriko'])

    last_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_LastName11']")))
    last_name.send_keys(['Herron Jr.'])

    zipcode = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_ZipCode12']")))
    zipcode.send_keys(['33065'])

    driver.save_screenshot('ZipCode.png')

    email_address = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_EmailAddress13']")))
    email_address.send_keys(['testacctmanager24@gmail.com'])

    phone_number = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_PhoneNumber14']")))
    phone_number.send_keys(['5612064658'])

    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input_Password15']")))
    password.send_keys(['Admin123!'])

    show_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div[2]/div/form/div[2]/div[6]/div[1]/div[1]/div/label")))
    show_password.click()
    
    join_now = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Join now']")))
    join_now.click() 

    sms = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='phone-verification']/div/div/form/fieldset/div/div[1]/div[1]")))
    sms.click()

    next = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']")))
    next.click()

    time.sleep(3)