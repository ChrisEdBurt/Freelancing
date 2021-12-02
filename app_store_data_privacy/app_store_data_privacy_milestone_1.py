from bs4 import BeautifulSoup
import requests
import csv
from time import sleep, strftime
from numpy import e
from pandas import read_excel
from datetime import datetime

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

historic_data = 'NoHistData'

app_privacy_items = []
temp_items = []
linked_data_id = 0
linked_data_id_found = False

start_time = datetime.now()

try:
    print("")
    print("Getting Records.......")
    for count, value in enumerate(app_ids):

        page = requests.get(f"https://apps.apple.com/us/app/id{value}")
        soup = BeautifulSoup(page.content, 'html.parser')
        if ((count + 1) % 25 == 0):
            print(f"Record {count} Scraped...")

        temp_items.sort()
        temp_items.insert(0,historic_data)
        temp_items.insert(0,country_row[count])
        temp_items.insert(0,id_row[count])
        app_privacy_items.append(temp_items)
        temp_items = []

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
    print("Hours:Minutes:Seconds: ")
    print(str(total_time))

except Exception as e:
    print(e)

try:
    print("")
    print("Writing to CSV")
    with open('app_store_data_item.csv', 'a', newline='', encoding='utf-8') as f:
        header = ['App_ID','User Country', 'Version_History','DataUsedtoTrackYou','DataNotLinkedtoYou','NoDetailsProvided','DataLinkedtoYou','DataNotCollected']
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for item in app_privacy_items:
            writer.writerow(item)

    print("")
    print("Finished")

except Exception as e:
    print(e)