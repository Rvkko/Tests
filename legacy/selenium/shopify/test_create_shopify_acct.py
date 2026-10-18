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



def test_login_logout(driver, test_data):
    driver, wait = driver
    driver.get('https://www.shopify.com/')
    
    
    login = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div/div/div/div[2]/ul[1]/li[1]/a")))
    login.click()
    
    
    sign_up = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='body-content']/div[2]/div/div[2]/div/div/div/div[2]/div/p/a")))
    sign_up.click()
    
    signup_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='body-content']/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]/a[1]")))
    signup_email.click()

    email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_email']")))
    email.send_keys(test_data['email'])
    
    
    firstname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_first_name']")))
    firstname.send_keys(test_data['firstname'])
    
    
    lastname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_last_name']")))
    lastname.send_keys(test_data['lastname'])
    
    
    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='account_password']")))
    password.send_keys(test_data['strongerpassword'])
    
    
    cfrm_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password-confirmation']")))
    cfrm_password.send_keys(test_data['strongerpassword'])
    
    
    create_account = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submit-disable']/button")))
    create_account.click()
