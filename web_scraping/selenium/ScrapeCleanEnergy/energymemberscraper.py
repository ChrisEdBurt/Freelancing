from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from lxml import html
from time import sleep
import csv
from pprint import pprint
import re

num_regx = re.compile('[0-9]{1,3}')

temp_details = ""
catergory_list = []
view_all = sponsoring = corporate = professional_services = associate = network = emerging_technologies = ""

results_filename = 'results.xlsx'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.cleanenergycouncil.org.au/membership/current-members')
sleep(1)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

member_categories = driver.find_elements_by_xpath("//ul[@class='search__filters']")
for cat in member_categories:
    temp_details = temp_details + str(cat.text.split('\n'))

cat_numbers = re.findall(num_regx, temp_details)
view_all =  "View All " + cat_numbers[0]
sponsoring = "Sponsoring " + cat_numbers[1]
corporate = "Corporate " + cat_numbers[2]
professional_services = "Professional Services " + cat_numbers[3]
associate = "Associate " + cat_numbers[4]
network = "Network " + cat_numbers[5]
emerging_technologies = "Emerging_technologies " + cat_numbers[6]

company_name = driver.find_element_by_xpath("//p[@class='h4 card-accordion__heading']")
company_summary = driver.find_element_by_xpath("//p[@class='card-accordion__summary']")
company_headings = driver.find_elements_by_xpath("//div[@class='h6 card-accordion__content-block-heading']")

print(company_name.text)