from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep

fireFoxOptions = Options()  
fireFoxOptions.add_argument("--headless") 
fireFoxOptions.add_argument("--window-size=1920,1080")
fireFoxOptions.add_argument('--start-maximized')
fireFoxOptions.add_argument('--disable-gpu')
fireFoxOptions.add_argument('--no-sandbox')

article_list = []

driver = webdriver.Firefox(options=fireFoxOptions)

driver.get('https://forbes.com')

search_button = driver.find_element_by_xpath("//button[@class='icon--search']").click()
sleep(1)

search_input = driver.find_element_by_xpath("//input[@class='search-modal__input']")
search_input.send_keys("Bitcoin")
search__submit_button = driver.find_element_by_xpath("//button[@class='search-modal__submit']").click()
sleep(1)

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')
reviews = []
articles = soup.find_all('a', class_='stream-item__title')
for article in articles:

    article_title = article.get_text()
    article_title_link = article['href']

    article_list.append(i.text + "," + article_title_link)

print(article_list)