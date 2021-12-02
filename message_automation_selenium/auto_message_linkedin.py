from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver = webdriver.Chrome()
driver.get("http://www.linkedin.com")

time.sleep(2)

username = driver.find_element_by_xpath("//input[@name='session_key']")
password = driver.find_element_by_xpath("//input[@name='session_password']")

username.send_keys('****')
password.send_keys('****')

submit = driver.find_element_by_xpath("//button[@class='sign-in-form__submit-button']").click()

driver.get("https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH")
time.sleep(2)

all_buttons = driver.find_element_by_tag_name("button")
message_buttons = [btn for btn in all_buttons if btn.text == "Message"]

for i in range(len(message_buttons)):

    driver.execute_script("arguments[0].click()", message_buttons[i])
    time.sleep(2)
    main_div = driver.find_element_by_xpath("//div[starts-with(@class, 'msg-form__msg-content-container')]")
    driver.execute_script("arguments[0].click()", main_div)

    paragraps = driver.find_elements_by_tag_name("p")
    print(paragraps[:-5].text)

    time.sleep(2)
    close_button = driver.find_element_by_xpath("//button[starts-with(@data-control-name','overlay.close_conversation_window')]").click()
    driver.execute_script("arguments[0].click()", close_button)
    time.sleep(2)