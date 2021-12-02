import re
import csv
from time import sleep
from types import new_class
from bs4 import BeautifulSoup
import requests

template = 'https://news.search.yahoo.com/search?p={}'

url = template.format("iphone 12 leaked")

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

news_cards = soup.find('div', 'Main')
print(news_cards)