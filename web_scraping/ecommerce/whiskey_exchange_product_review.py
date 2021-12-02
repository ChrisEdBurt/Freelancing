import requests
from bs4 import BeautifulSoup
import lxml

baseurl = 'http://www.thewhiskeyexchange.com/'

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"}
http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

productlinks = []

for x in range(1,6):
    page = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}&psize=24&sort=pasc', headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    productlist = soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        print(item)

print(len(productlinks))