from os import popen
from bs4 import BeautifulSoup
import requests
import csv
from time import perf_counter, sleep, strftime
from numpy import e
from pandas import read_excel
from datetime import datetime
import json

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

historic_data = 'NA'

app_privacy_items = []
temp_items = []
linked_data_id = 0
linked_data_id_found = False

start_time = datetime.now()

try:
    print("")
    print("Getting Records.......")
    for count, value in enumerate(app_ids[0:1]):
        print("app id: " + str(count))

        capture_response = requests.get(f"http://web.archive.org/cdx/search/cdx?url=apps.apple.com/us/app/id{value}&fl=timestamp,original&output=json&limit=999")

        captured_urls = json.loads(capture_response.text)

        for captured_counter, captured_value in enumerate(captured_urls):
            print("captured_counter: " + str(captured_counter))

            captured_url = "https://web.archive.org/web/" + str(captured_urls[captured_counter][0]) + "if_/" + str(captured_urls[captured_counter][1])
            captured_url = requests.get(captured_url)

            soup = BeautifulSoup(captured_url.text, 'html.parser')

            data_card = soup.find_all("div", {"class": "app-privacy__card"})

            for card_count, card_value in enumerate(data_card):
                print("card_count: " + str(card_count))
                data_type = card_value.find_all("h3", {"class": "privacy-type__heading"})
                print("data_type")
                
                for data_type_count, data_type_value in enumerate(data_type):
                    print("data_type_count: " + str(data_type_count))

                    if linked_data in data_type_value.text:
                        print("linked_data")
                        linked_data_id = data_type_count

                        found_data_headings = data_card[linked_data_id].find_all("span", {"class": "privacy-type__grid-content privacy-type__data-category-heading"})
                        for i in found_data_headings:
                            temp_items.append(i.text)
                            print("found_data_headings")

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
        header = [
        'App ID','User Country','Time(Historic Data)','Browsing History', 'Contact Info', 'Contacts', 'Diagnostics', 'Financial Info', 'Identifiers', 'Location', 'Other Data', 'Purchases', 'Search History', 'Usage Data', 'User Content']
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for item in app_privacy_items:
            writer.writerow(item)

    print("")
    print("Finished")

except Exception as e:
    print(e)