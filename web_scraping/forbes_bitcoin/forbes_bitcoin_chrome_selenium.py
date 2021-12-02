from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

chrome_options = Options()

chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2 }) 

article_list = []

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://forbes.com')

search_button = driver.find_element_by_xpath("//button[@class='icon--search']").click()
sleep(1)

search_input = driver.find_element_by_xpath("//input[@class='search-modal__input']")
search_input.send_keys("Bitcoin")
search__submit_button = driver.find_element_by_xpath("//button[@class='search-modal__submit']").click()
sleep(1)

article_titles = driver.find_elements_by_xpath("//a[@class='stream-item__title']")

for i in article_titles:
    article_title_link = i.get_attribute('href')
    article_list.append(i.text + "," + article_title_link)

print(article_list)