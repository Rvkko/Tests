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
from selenium.common.exceptions import NoSuchElementException




def test_login_logout(driver, test_data):
    driver, wait = driver
    driver.get('https://www.shopify.com/')
    
    pricing = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div/div/div/nav/ul/li[2]/div/a")))
    pricing.click()
    
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    
    full_features = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/section[2]/section[2]/section/div[1]/button")))
    full_features.click()
    
    features = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/section[2]/section[2]/section/div[2]/section')))
    assert features.is_displayed(), "Pricing feature comparison did not become visible"
