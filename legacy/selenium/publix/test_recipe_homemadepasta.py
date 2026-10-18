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
    driver.get('https://www.publix.com/')

    search_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInputFlyout"]')))
    search_input.send_keys('All-Purpose Flour')

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navBar']/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/form/button[2]")))
    search_button.click()

    add_to_list_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='add-to-list-btn-123-11256']")))
    add_to_list_button.click()

    clear_search_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchInputFlyout"]')))
    clear_search_input.click()
    clear_search_input.clear()

    eggs = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInputFlyout"]')))
    eggs.send_keys(['Eggs']) 

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navBar']/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/form/button[2]")))
    search_button.click()
    
    
    add_to_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='add-to-list-btn-140-303494']/span[2]")))
    add_to_list.click()

    clear_search_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchInputFlyout"]')))
    clear_search_input.click()
    clear_search_input.clear()   

    olive_oil = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInputFlyout"]')))
    olive_oil.send_keys(['Olive Oil'])

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navBar']/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/form/button[2]")))
    search_button.click()

    add_to_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='add-to-list-btn-126-10898']")))
    add_to_list.click()

    clear_search_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchInputFlyout"]')))
    clear_search_input.click()
    clear_search_input.clear()    

    salt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInputFlyout"]')))
    salt.send_keys(['Salt'])  

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navBar']/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/form/button[2]")))
    search_button.click()

    add_to_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='add-to-list-btn-126-9450']")))
    add_to_list.click()

    #Verifying Items Have Been Added To Shopping List
    shopping_list = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='userShoppingList']/span[2]")))
    shopping_list.click()
