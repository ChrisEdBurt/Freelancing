from datetime import datetime, timedelta
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def print_welcome_message():
    print()
    print("Welcome to the Grand Exchange Scraping Tool")
    print("Please Enter one of the optons below.")
    print()
    print("Enter 1 to scrape the Grand Exchange for 'Price Rises'")
    print("Enter 2 to scrape the Grand Exchange for 'Price Falls'")
    print("Enter 3 to scrape the Grand Exchange for 'Most Valuable Trades'")
    print("Enter 4 to scrape the Grand Exchange for 'Most Traded'")

def print_time_period_message():
    print("")
    print("Please enter the time period in which you want the scraping to repeat.")
    print("Entering 0 will result in only scrape the Grand Exchange once and then the program will exit.")
    print("Entering a number greater than 0 will repeat the scraping at that interval, indefinitely.")

def write_to_csv(results_filename, ge_item_data, first_scraping):
# Saving the data in a CSV format with the current date, time as well as which category was scraped.
    with open(results_filename, 'a', newline='', encoding='utf-8') as f:
        header = ['Name','Membership','Min Price','Max Price','Median Price','Total Daily Trade Value']
        writer = csv.writer(f, delimiter=',')
        if first_scraping == True:
            writer.writerow(header)
        for item in ge_item_data:
            writer.writerow(item)
    print("Writing scraped Grand Exchange data to csv file.")
    print(f"The name of that file is {results_filename}")

def append_item_records(item_list_category, item_list_length, ge_item_data, ge_item_field_data):
    print(f"Begin Grand Exchange Scraping of {item_list_category}")
    for item in range(1, item_list_length+1):
        for item_group in range(1, 7):    

            item_tr = f'//*[@id="grandexchange"]/div/div/main/div[2]/table/tbody/tr[{item}]/td[{item_group}]'
            
            item_info = driver.find_element_by_xpath(item_tr).text

            if item_group == 2:          
                if item_info == "":
                    item_info = "N"
                else:
                    item_info = "Y"

            ge_item_field_data.append(item_info)
        ge_item_data.append(ge_item_field_data)
        ge_item_field_data = []
        if item % 5 == 0:
            print(f"Add record {item} of {item_list_length}")

    print("")
    print(f"Completed item records collection of {item_list_category}")
    
# TODO Allow scraping of item based user search, will require custom request to get around Incapsula
url_most_traded = 'https://secure.runescape.com/m=itemdb_oldschool/top100?list=0'
url_most_valuable_trades = 'https://secure.runescape.com/m=itemdb_oldschool/top100?list=1'
url_price_rises = 'https://secure.runescape.com/m=itemdb_oldschool/top100?list=2'
url_price_falls = 'https://secure.runescape.com/m=itemdb_oldschool/top100?list=3'

print_welcome_message()

first_scraping = True
scraping_complete = False
scraping_time_period = 1
valid_option = False

while scraping_complete == False:
    while valid_option == False:
        selection = input()

        # Navigates to the 100 Price Rises Items page
        if selection == '1':
            options = Options()
            options.add_argument("window-size=1280,1000")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url_price_rises)
            item_list_category = "Price-Rises"
            results_filename = item_list_category + '-' + str(datetime.now().strftime('%m-%d-%Y-%H-%M-%S')) + '.csv'
            valid_option = True

        # Navigate to the 100 Price Falls Items page
        elif selection == '2':
            options = Options()
            options.add_argument("window-size=1280,1000")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url_price_falls)
            item_list_category = "Price-Falls"
            results_filename = item_list_category + '-' + str(datetime.now().strftime('%m-%d-%Y-%H-%M-%S')) + '.csv'
            valid_option = True

        # Navigate to the 100 Most Valuable Items page
        elif selection == '3':
            options = Options()
            options.add_argument("window-size=1280,1000")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url_most_valuable_trades)
            item_list_category = "Most-Valuable-Trades"
            results_filename = item_list_category + '-' + str(datetime.now().strftime('%m-%d-%Y-%H-%M-%S')) + '.csv'
            valid_option = True

        # Navigate to the 100 Most Traded Items page
        elif selection == '4':
            options = Options()
            options.add_argument("window-size=1280,1000")
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url_most_traded)
            item_list_category = "Most-Traded"
            results_filename = item_list_category + '-' + str(datetime.now().strftime('%m-%d-%Y-%H-%M-%S')) + '.csv'
            valid_option = True

        # # Invalid choice, prompts user to try again.
        else:
            time.sleep(1)
            print("")
            print("Please make a valid selection of one of the four choices.")

    print_time_period_message()

    valid_time_period = False
    while valid_time_period != True:
        selection = input()
        
    # Error handling for selected time period
        if selection == '0':
            print("")
            print("Scraping will commence once and then exit.")
            print("")
            time.sleep(3)
            scraping_complete = True
            valid_time_period = True
            
        elif int(selection) > 0:
            print(f"Scraping will commence every {selection} minute\\s")
            scraping_time_period = selection
            valid_time_period = True

        else:
            time.sleep(1)
            print("")
            print("Please make a valid selection of ether 0 or greater than 0")
    
    ge_item_field_data = []
    ge_item_data = []
    item_info = f''

    item_list_length = 100

    append_item_records(item_list_category, item_list_length, ge_item_data, ge_item_field_data)
    write_to_csv(results_filename, ge_item_data, first_scraping)

    current_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    time_plus_time_period = (datetime.now() + timedelta(minutes=int(scraping_time_period)))

    if scraping_complete != True:
        while time_plus_time_period > current_time:
            current_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            print("Time until next scraping in " + str(time_plus_time_period - current_time))
            time.sleep(5)
            url = driver.current_url

    while scraping_complete == False:
        print("Scraping will now commence again")
        first_scraping = False
        driver.close()
        options = Options()
        options.add_argument("window-size=1280,1000")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        append_item_records(item_list_category, item_list_length, ge_item_data, ge_item_field_data)
        write_to_csv(results_filename, ge_item_data, first_scraping)

        ge_item_field_data = []
        ge_item_data = []

        current_time = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
        time_plus_time_period = (datetime.now() + timedelta(minutes=int(scraping_time_period)))
    
print("")
print("Scraping has been completed.")
print("Program will now exit")
driver.close()