import json
import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10) 
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
    driver.get('https://www.shopify.com/')
    
    driver.save_screenshot("homepage.png")
    
    login = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div/div/div/div[2]/ul[1]/li[1]/a")))
    login.click()
    
    driver.save_screenshot("login page.png")
    
    sign_up = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='body-content']/div[2]/div/div[2]/div/div/div/div[2]/div/p/a")))
    sign_up.click()
    
    signup_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='body-content']/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]/a[1]")))
    signup_email.click()

    email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_email']")))
    email.send_keys(test_data['email'])
    
    driver.save_screenshot("email.png")
    
    firstname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_first_name']")))
    firstname.send_keys(test_data['firstname'])
    
    driver.save_screenshot("firstname.png")
    
    lastname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_last_name']")))
    lastname.send_keys(test_data['lastname'])
    
    driver.save_screenshot("lastname.png")
    
    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_password']")))
    password.send_keys(test_data['strongerpassword'])
    
    driver.save_screenshot("password.png")
    
    cfrm_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password-confirmation']")))
    cfrm_password.send_keys(test_data['strongerpassword'])
    
    driver.save_screenshot("condirmpassword.png")
    
    create_account = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submit-disable']/button")))
    create_account.click()
    
    driver.save_screenshot("create account.png")

