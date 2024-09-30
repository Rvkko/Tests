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

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.3))

def test_login(driver, test_data):
    driver, wait = driver
    driver.get('https://www.shopify.com/')

    login_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in")))
    login_button.click()

    username = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='account_email']")))
    username.send_keys(test_data['email'])

    continue_bttn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='commit']")))
    continue_bttn.click()
    
    time.sleep(2)

    password = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='account_password']")))
    password.send_keys(test_data['strongerpassword'])

    login_bttn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='login_form']/div[2]/div[4]/button")))
    login_bttn.click()

    product_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/store/ecf120-bf/products']")))
    product_button.click()

    no_products_message_xpath = "//*[@id='AppFrameScrollable']/div/div/div/div[2]/div/div/div/div[2]/div/div/div"
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, no_products_message_xpath)))
        print("No products found. Creating a new product.")
        product_add(wait, test_data)
    except Exception:
        print("No product found. Create a new one.")

    # Call functions to create additional products
    create_shorts_product(wait, test_data)
    create_mens_pants_product(wait, test_data)
    create_womans_pants_product(wait, test_data)

def product_add(wait, test_data):
    product_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/a")))
    product_add.click()

    product_title = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='title']")))
    product_title.send_keys(test_data['shirts-title'])

    category = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='productTaxonomyNodeId']")))
    category.send_keys("Apparel & Accessories")

    product_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='price']")))
    product_price.send_keys("19.99")

    compare_at_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='compareAtPrice']")))
    compare_at_price.send_keys("20")

    cost_per_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='unitCost']")))
    cost_per_item.send_keys("15")

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[2]/form/div/div[3]/div/div/button")))
    save.click()

    back_arrow = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[1]/div/a")))
    back_arrow.click()

    driver.refresh()

def create_shorts_product(wait, test_data):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, f"//h3[contains(text(),'{test_data['shirts-title']}')]")))
        print(f"Product '{test_data['shirts-title']}' already exists.")
    except:
        print(f"Product '{test_data['shorts-title']}' does not exist. Creating a new one.")

        

    product_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/a")))
    product_add.click()

    product_title = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='title']")))
    product_title.send_keys(test_data["shorts-title"])

    category = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='productTaxonomyNodeId']")))
    category.send_keys("Apparel & Accessories")

    product_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='price']")))
    product_price.send_keys("19.99")

    compare_at_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='compareAtPrice']")))
    compare_at_price.send_keys("20")

    cost_per_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='unitCost']")))
    cost_per_item.send_keys("15")

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[2]/form/div/div[3]/div/div/button")))
    save.click()

    back_arrow = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[1]/div/a")))
    back_arrow.click()

def create_mens_pants_product(wait, test_data):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, f"//h3[contains(text(),'{test_data['shirts-title']}')]")))
        print(f"Product '{test_data['shorts-title']}' already exists.")
    except:
        print(f"Product '{test_data['men-pants-title']}' does not exist. Creating a new one.")

    product_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/a")))
    product_add.click()

    product_title = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='title']")))
    product_title.send_keys(test_data["men-pants-title"])

    category = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='productTaxonomyNodeId']")))
    category.send_keys("Apparel & Accessories")

    product_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='price']")))
    product_price.send_keys("19.99")

    compare_at_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='compareAtPrice']")))
    compare_at_price.send_keys("20")

    cost_per_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='unitCost']")))
    cost_per_item.send_keys("15")

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[2]/form/div/div[3]/div/div/button")))
    save.click()

    back_arrow = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[1]/div/a")))
    back_arrow.click()

def create_womans_pants_product(wait, test_data):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, f"//h3[contains(text(),'{test_data['shirts-title']}')]")))
        print(f"Product '{test_data['men-pants-title']}' already exists.")
    except:
        print(f"Product '{test_data['woman-pants-title']}' does not exist. Creating a new one.")

    product_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/a")))
    product_add.click()

    product_title = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='title']")))
    product_title.send_keys(test_data["woman-pants-title"])

    category = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='productTaxonomyNodeId']")))
    category.send_keys("Apparel & Accessories")

    product_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='price']")))
    product_price.send_keys("19.99")

    compare_at_price = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='compareAtPrice']")))
    compare_at_price.send_keys("20")

    cost_per_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='unitCost']")))
    cost_per_item.send_keys("15")

    save = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[2]/form/div/div[3]/div/div/button")))
    save.click()

    back_arrow = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='AppFrameScrollable']/div/div/div/div[1]/div[2]/div/div[1]/div/a")))
    back_arrow.click()