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
    wait = WebDriverWait(driver, 10)  # Increased wait time for reliability
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
    
    element_to_hover_over = driver.find_element(By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/div/button/div")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()

    time.sleep(6)

    create_acct = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/nav/div/div/div[2]/a")))
    create_acct.click()

    firstname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='firstName']")))
    firstname.send_keys(test_data['firstname'])

    email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='signupEmail']")))
    email.send_keys(test_data['email'])

    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='signupPassword']")))
    password.send_keys(test_data['password'])

    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

    confirm_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='signupConfirmPassword']")))
    confirm_password.send_keys(test_data['confirmpassword'])

    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

    gender = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gender']")))
    gender.click()

    time.sleep(2)
    gender_selection = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gender']/option[2]")))
    gender_selection.click()

    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

    home_page = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[1]/a[3]")))
    home_page.click()
    
    signup_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuMemberSignUpForm-contentTop-98a05382-e397-4cac-99ce-5cb860bdc37b']/div/div[2]/div/div[2]/form/div[8]/button")))
    signup_button.click()

    login_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginEmail']")))
    login_email.send_keys(test_data['email'])
        
    login_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginPassword']")))
    login_password.send_keys(test_data['password'])

    login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuMemberSignInForm-contentTop-d0b8f76c-2b3f-4762-8b02-26846c276f5c']/div/div[2]/form/div[4]/button")))
    login_submit.click()

    # Proceed to premium subscription
    premium_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/div/a")))
    premium_button.click()

    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

    sevenday = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraSubscriptionPage-contentTop-4440d133-553c-4a38-a144-f52c6190c78d']/div/div[1]/div[3]/section[2]/div/button")))
    sevenday.click()

    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Recipient First Name']")))
    first_name.send_keys(test_data['firstname'])

    lastname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Recipient Last Name']")))
    lastname.send_keys(test_data['lastname'])

    address = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div/div/input")))
    address.send_keys(test_data['address'])

    address_click = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div/div/div/button[1]")))
    address_click.click()

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[4]/button")))
    next_button.click()

    card_number = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-creditCardNumber']")))
    card_number.send_keys(test_data['cardinfo'])

    expiration_month = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-creditCardExpirationMonth']")))
    expiration_month.click()

    expiration_month_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-creditCardExpirationMonth']/option[10]")))
    expiration_month_select.click()

    expiration_year = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-creditCardExpirationYear']")))
    expiration_year.click()

    expiration_year_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-creditCardExpirationYear']/option[8]")))
    expiration_year_select.click()

    cvv = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-cardSecurityCode']")))
    cvv.send_keys(test_data['cvv'])

    # Handle CAPTCHA - if needed
    try:
        imnotarobot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']/div[1]")))
        imnotarobot.click()
    except TimeoutException:
        print("CAPTCHA might require manual intervention.")

    add_card_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submitButton']")))
    add_card_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains('https://weather.com/'))
    actual_url = driver.current_url
    assert actual_url.startswith('https://weather.com/')
