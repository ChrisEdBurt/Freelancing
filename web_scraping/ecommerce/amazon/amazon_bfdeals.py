from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas

s = HTMLSession()

productlist = []
searchterm = 'ultrawide monitor'
url = f'https://www.amazon.com/s?k={searchterm}'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getproducts(soup):

    products = soup.find_all('div', {'data-component-type: "s-search-result'})
    for item in products:
        title = item.find('a', {'class: a-link-normal a-text-normal'})['href'].text.strip()
        short_title = item.find('a', {'class: a-link-normal a-text-normal'})['href'].text.strip()[:25]
        link = item.find('a', {'class: a-link-normal a-text-normal'})['href']
        try:
            saleprice = item.find('span', {'class:' 'a-offscreen'})[0].text.replace('$','').strip()
        except:
            saleprice = 0

        try:
            reviews = item.find('span', {'class:' 'a-size-base'}).text.strip()
        except:
            reviews = ''

        productitem = {
            'title': title,
            'short_title': short_title,
            'link':link,
            'saleprice':saleprice,
            'reviews':reviews
        }
        productitem.append(productitem)
    print(productlist)

def getnextpage(souup):
    pages = soup.find('ul', {'class:' 'a-pagination'})
    if not soup.find('li', {'class:' 'a-last'}):
        url = 'https://www.amazon.com' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

data = getdata(url)

r = s.get(url)
r.html.render(sleep=1)
soup = BeautifulSoup(r.html.html, 'html.parser')

getproducts(soup)