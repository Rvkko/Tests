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
    driver.get('https://www.youtube.com/')

    driver.save_screenshot("YT_Homepage.png")

    sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620']")))
    sign_in.click()

    time.sleep(2)
    driver.save_screenshot("Signin_Page.png")

    email = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    email.send_keys('testacctmanager24@gmail.com')

    time.sleep(2)
    driver.save_screenshot("Email_Cred.png")

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")))
    next_button.click()

    password = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    password.send_keys('Admin123!')

    driver.save_screenshot("Password_Cred.png")

    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and .//span[text()='Next']]")))
    next_button.click()

    time.sleep(2)
    driver.save_screenshot("YT_Homepage.png")

    search_bar = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='search']")))
    search_bar.send_keys('java full course for free')

    driver.save_screenshot("Video_Search.png")

    search = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='search-icon-legacy']")))
    search.click()

    driver.save_screenshot("Video_click.png")

    video = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@src='https://i.ytimg.com/vi/xk4_1vDrzzo/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDIGC1UnH_XVz5NaWdKYCpeXLuUYQ']")))
    video.click()

    mute_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Mute (m)']")))
    mute_button.click()    

    like_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='I like this']")))
    like_button.click()

    driver.save_screenshot("I_like_this.png")

    share_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading']")))
    share_button.click()

    driver.save_screenshot("Share_Button.png")
    
    copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Copy']")))
    copy_button.click()

    driver.save_screenshot("Copy_link.png")

    driver.get('https://mail.google.com/mail/u/0/#inbox')

    driver.save_screenshot("Gmail_Homepage.png")

    compose_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@gh='cm']")))
    compose_button.click()

    driver.save_screenshot("Create_Email.png")

    recepient_text = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='agP aFw']")))
    recepient_text.send_keys(['derrikoherronjr91@gmail.com'])

    driver.save_screenshot("Recepient.png")

    hovercard = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-hovercard-id='derrikoherronjr91@gmail.com']")))
    hovercard.click()

    subject_text = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='subjectbox']")))
    subject_text.send_keys(['Funny Video XD'])

    driver.save_screenshot("Subject_Text.png")

    body_text = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='Am aiL Al editable LW-avf tS-tW']")))
    body_text.send_keys(['https://youtu.be/xk4_1vDrzzo?si=5574txoSannLPTVj'])

    driver.save_screenshot("Body_Text.png")

    send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")))
    send_button.click()

    driver.save_screenshot("Send_Button.png")

    WebDriverWait(driver, 5).until(EC.url_contains('https://mail.google.com/mail/'))
    actual_url = driver.current_url
    assert actual_url.startswith('https://mail.google.com/mail/')