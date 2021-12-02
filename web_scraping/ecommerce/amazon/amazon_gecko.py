from logging import disable
from pathlib import Path
import csv

from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = str(Path('geckodriver').resolve())
BROWSER = webdriver.Firefox(executable_path=DRIVER_PATH)

def write_csv(products):

    for product in products:
        print(product)

    with open('results.csv', 'a') as f:
        fields = ['title', 'price', 'url']

        writer = csv.DictWriter(f, fieldnames=fields)

        for product in products:
            try:
                writer.writerow(product)
            except:
                writer.writerow("N/A DATA")

def get_html(url):
    BROWSER.get(url)
    return BROWSER.page_source

def get_date(product):
    try:
        h2 = product.h2
    except:
        title = ''
        url = ''
    else:
        title = h2.text.strip()
        url = h2.a.get('href')
    
    try:
        price = product.find('span', class_='a-price-whole').text.strip('.').strip()
    except:
        price = ''

    data = {'title': title, 'url': url, 'price': price}

    return data


def scrape():
        url = 'https://www.amazon.com/ultrawide-monitor/s?k=ultrawide+monitor&page=1&qid=1623705853&ref=sr_pg_2'
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        page_number_parent = soup.find('ul', class_= 'a-pagination')
        page_number = page_number_parent.find_all('li', {'aria-disabled': 'true'}, class_= 'a-disabled')
        for pag_num in page_number:
            if '...' not in pag_num:
                page_number = pag_num.text.strip()
                page_number = int(page_number) + 1

        product_data = []

        for i in range(2, page_number):
            url = f'https://www.amazon.com/ultrawide-monitor/s?k=ultrawide+monitor&page={i}&qid=1623705853&ref=sr_pg_2'
            html = get_html(url)

            soup = BeautifulSoup(html, 'lxml')
            products = soup.find_all('div', {'data-asin': True, 'data-component-type': 's-search-result'})

            for product in products:
                data = get_date(product)
                product_data.append(data)

        write_csv(product_data)

scrape()