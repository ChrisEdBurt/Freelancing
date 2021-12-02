from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
from pprint import pprint
import csv

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2 }) 

product_details = []

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

driver.get('https://autoepcservice.com/product/clark-forklift-updated-2020-full-service-operators-maintenance-schematic-manuals-service-bulletins-15-87gb-dvd-pdf/')

desc = driver.find_element_by_xpath("//div[@id='tab-description']")
product_details = desc.text.split('\n')
pprint(product_details)

results_filename = "machine_specs" + str(datetime.now().strftime('%m-%d-%Y-%H-%M-%S')) + '.csv'
write_to_csv(results_filename, product_details)

driver.close()