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
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

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
    driver.get('https://weather.com/')

    element_to_hover_over = driver.find_element(By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/div/button/div")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()

    create_acct = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/nav/div/div/div[2]/a")))
    create_acct.click()

    time.sleep(6)

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

    gender_selection = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gender']/option[2]")))
    gender_selection.click()

    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

    time.sleep(5)

    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()


    signup = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuMemberSignUpForm-contentTop-98a05382-e397-4cac-99ce-5cb860bdc37b']/div/div[2]/div/div[4]/form/div[8]/button"))) 
    signup.click()

    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

    time.sleep(4)

    home_page = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[1]/a[3]")))
    home_page.click()

    element_to_hover_over = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/div/button/div")))
    wait.until(EC.visibility_of(element_to_hover_over))
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log In']")))
    login_button.click()

    time.sleep(6)

    login_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginEmail']")))
    login_email.send_keys(test_data['email'])

    login_password = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='loginPassword']")))
    login_password.send_keys(test_data['password'])

    login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuMemberLRLoginForm-contentTop-06cbec75-5893-4d34-9ff4-a1474a120f9d']/div/div[4]/form/div[3]/button")))
    login_submit.click()

    time.sleep(5)

    premium_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba']/header/div/div[2]/div[3]/div/a")))
    premium_button.click()

    #Viewing Details of premium
    
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()

    sevenday = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraSubscriptionPage-contentTop-4440d133-553c-4a38-a144-f52c6190c78d']/div/div[1]/div[3]/section[2]/div/button")))
    sevenday.click()

    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Recipient First Name']")))
    first_name.send_keys(test_data['firstname'])

    lastname = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Recipient Last Name']")))
    lastname.send_keys(test_data['lastname'])

    manual_address = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[3]/button")))
    manual_address.click()

    address = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div[1]/div/input")))
    address.send_keys(test_data['address'])

    city = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div[3]/div[1]/div/input")))
    city.send_keys(test_data['city'])

    state = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div[3]/div[2]/div[1]/select")))
    state.click()

    state_selection = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div[3]/div[2]/div[1]/select/option[13]")))
    state_selection.click()

    zipcode = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='WxuZuoraCheckoutPage-contentTop-f91cc90c-40b5-4896-b3f3-f8ae78bd7d76']/div/div[3]/div[1]/section[2]/div/div/div[2]/div[3]/div[3]/div/input")))
    zipcode.send_keys(test_data['zip'])

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

    try:
        imnotarobot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']/div[1]")))
        imnotarobot.click()
    except TimeoutException:
        print("CAPTCHA might require manual intervention.")

    add_card_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submitButton']")))
    try:
        add_card_button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", add_card_button)

    WebDriverWait(driver, 10).until(EC.url_contains('https://weather.com/'))
    actual_url = driver.current_url
    assert actual_url.startswith('https://weather.com/')