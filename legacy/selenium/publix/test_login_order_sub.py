import json
import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def test_login_logout(driver, test_data):
    driver, wait = driver
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()
    driver.get('https://www.publix.com/')
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="userLogIn"]')))
    login_button.click()
    
    username = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='signInName']")))
    username.send_keys(test_data['email'])
    
    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password']")))
    password.send_keys(test_data['password'])

    rmbr_me = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='localAccountForm']/div[3]/div[4]/label")))
    rmbr_me.click()

    login = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login.click()
