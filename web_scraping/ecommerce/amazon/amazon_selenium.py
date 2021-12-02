from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
from time import sleep
import csv
from pprint import pprint
import re

def write_to_csv(results_filename, product_data):
    with open(results_filename, 'a', newline='', encoding='utf-8') as f:
        header = ['Title','Reviews','Price']
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for item in product_data:
            writer.writerow(item)

excluded_text = [
   "Sponsored",
   "Amazon'\\'s Choice",
   "Featured from our brands",
   "Best Seller",
   "Filter by price",
   "Under $25",
   "$25 to $50",
   "$50 to $100",
   "$100 to $200",
   "$200 & Above"
]

regx_single = re.compile('(\d,)([1-9]+)(\d,)')
regx_multi = re.compile('\d[0-9]+)(,)(\d[0-9]+)(\w,')

product = ""
product_temp = []

product_details = []

search_term = ""

results_filename = 'results.csv'

search_term = 'keyboard'

chrome_options = Options()

chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2 }) 

driver = webdriver.Chrome(options=chrome_options)

driver.get(f'https://www.amazon.com/s?k={search_term}')
sleep(1)

tree = html.fromstring(driver.page_source)

num_of_pages = tree.xpath('//li[contains(@aria-disabled, "true")]')
for i in num_of_pages:
    if i.text == "...":
        pass
    else:
        num_of_pages = int(i.text)

for page_num in range(1, 2):

    driver.get(f'https://www.amazon.com/s?k={search_term}&page={page_num}')
    sleep(1)

    product_tree = driver.find_elements_by_xpath('//div[contains(@data-cel-widget, "search_result_")]')

    for item in product_tree[1:2]:

        product = item.text.replace('\n', ',')
        if re.search(regx_single, product) != None:
            review_num = re.search(regx_single, product)
        elif re.search(regx_multi, product) != None:
            review_num = re.search(regx_multi, product)

        print(product)
        print(review_num.group())