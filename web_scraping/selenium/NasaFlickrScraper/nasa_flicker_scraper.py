from datetime import datetime, timedelta, date
from time import sleep
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Saving the data in a CSV format with the current date.
def write_to_csv(results_filename, image_data):
    with open(results_filename, 'w', newline='') as f:
        header = ['Label','URL']
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for item in image_data:
            writer.writerow(item)

    print(f"The name of image file is {results_filename}")

def scrape_images():
    today = date.today()
    today_date = today.strftime("%d-%m-%Y")
    chrome_options = Options()
    image_list = []
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.flickr.com/photos/nasacommons/')
    images = driver.find_elements_by_xpath("//a[@class='overlay']")
    # for image in images[2:]:
    for image in images:
        image_link = image.get_attribute('href')
        image_label = image.get_attribute('aria-label')
        image_list.append([[image_label],[image_link]])
    write_to_csv(f"NASAFlickrImages-{today_date}.csv", image_list)
scrape_images()