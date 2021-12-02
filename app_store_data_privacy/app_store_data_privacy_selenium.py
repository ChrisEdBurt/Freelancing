import csv
from time import sleep, strftime
from numpy import e, mod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import read_excel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, element

from datetime import datetime, timedelta
import time

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

my_sheet = 'Sheet1' 
file_name = 'AppIDList.xlsx'
df = read_excel(file_name, sheet_name = my_sheet)

app_ids = []
country_ids = []

no_identity_data = 'Data Not Linked to You'
tracking_data = 'Data Used to Track You'
linked_data = 'Data Linked to You'

country_row = df['user_country'].values
for country in country_row:
    country_ids.append(country)

id_row = df['app_id'].values
for item in id_row:
    app_ids.append(item)

historic_data = 'NONE'

app_privacy_items = []
temp_items = []
linked_id = 0

options = Options()
options.add_argument("window-size=1280,1000")
driver = webdriver.Chrome(chrome_options=options)

start_time = datetime.now()

print("")
print("Getting Records.......")
for count, value in enumerate(app_ids[0:50]):
    driver.get(f"https://apps.apple.com/us/app/id{value}")
    sleep(2)

    details_button = driver.find_element_by_xpath('//button[text()="See Details"]')
    details_button.click()
    sleep(3)
        
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "we-modal__content__wrapper")))

    details_modal = driver.find_element_by_xpath('//div[@class="we-modal__content__wrapper"]')
    modal_selector = driver.find_elements_by_xpath('//div[@class="app-privacy__modal-section"]')

    for modal_selector_count, modal_selector_value in enumerate(modal_selector):

        if linked_data in modal_selector[modal_selector_count].text:
            linked_id = modal_selector_count

            data_grids = modal_selector[linked_id].find_elements_by_xpath('//div[@class="privacy-type__grid"]')

            for data_grids_count, data_grids_value in enumerate(data_grids):
                item_string = str(data_grids_value.text).replace('\n',',')
                coma_index = item_string.index(',')
                item_string = replace_str_index(item_string, coma_index, ':')
                temp_items.append(item_string)
    
            temp_items.insert(0,historic_data)
            temp_items.insert(0,country_row[count])
            temp_items.insert(0,id_row[count])
            app_privacy_items.append(temp_items)
            temp_items = []

    print(f"Record {count} + Scraped")

end_time = datetime.now()

print("Start time: ") 
print(str(start_time))
print("End time:   ") 
print(str(end_time))
total_time = end_time - start_time
print(total_time)
total_time = str(total_time)
total_time = total_time[0:7]
print("Total time:")
print("Hour:Minutes:Seconds: ")
print(str(total_time))
    
print("")
print("Writing to CSV")
with open('app_store_data_item.csv', 'a', newline='', encoding='utf-8') as f:
    header = ['App_ID','Country Code','Historic Data','DataLinkedToYou']
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
    for item in app_privacy_items:
        if item == 'None':
            writer.writerow("")
        else:
            writer.writerow(item)

print("")
print("Finished")
driver.close()