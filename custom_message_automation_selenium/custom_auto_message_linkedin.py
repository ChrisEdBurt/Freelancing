from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get("http://www.linkedin.com")
time.sleep(2)

# search for login fields
username = driver.find_element_by_xpath("//input[@name='session_key']")
password = driver.find_element_by_xpath("//input[@name='session_password']")

# login details
username.send_keys('****')
password.send_keys('****')

submit = driver.find_element_by_xpath("//button[@class='sign-in-form__submit-button']").click()

driver.get('https://www.linkedin.com/search/results/people/?network=%5B%22S%22%5D&origin=FACETED_SEARCH')
time.sleep(2)

all_buttons = driver.find_elements_by_tag_name("button")
connect_buttons = [btn for btn in all_buttons if btn.text == "Connect"]

for btn in connect_buttons:
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)
    send_button = driver.find_element_by_xpath("//button[@aria=label='Send now']")
    driver.execute_script("arguments[0].click();", send_button)
    close_button = driver.find_element_by_xpath("//button[@aria=label='Dismiss']")
    driver.execute_script("arguments[0].click();", close_button)
    time.sleep(2)