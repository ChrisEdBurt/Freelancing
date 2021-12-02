import re
import csv
from getpass import getpass
from logging import Handler
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("window-size=1280,1000")
driver = webdriver.Chrome(chrome_options=options, executable_path=r"C:/Users/Work/Desktop/Work/Python\Web Scraping/chromedriver.exe")
driver.get('http://www.twitter.com/login')

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
username.send_keys('****')

password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
password.send_keys('****')
password.send_keys(Keys.RETURN)

try:
    # Getting current URL
    get_url = driver.current_url
    acc_check_url = "https://twitter.com/login?email_disabled=true&redirect_after_login=%2F"
    if acc_check_url in get_url:
        # sleep(100)
        username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username.send_keys('0274104689')
        password = driver.find_element_by_xpath('//input[@name="session[password]"]')
        password.send_keys('Password!')
        password.send_keys(Keys.RETURN)
        # driver.fullscreen_window()
except:
    "No Account Check"

sleep(2)
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys('#meme')
search_input.send_keys(Keys.RETURN)

sleep(2)
# navigate to historical 'latest' tab
driver.find_element_by_link_text('Latest').click()

sleep(2)
tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

def get_tweet_data(tweet):
    # tweet username
    username = tweet.find_element_by_xpath('.//span').text
    # twitter handle
    try:
        handle = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return
    try:
        # post date
        postdate = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    # tweet body
    try:
        comment = tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except NoSuchElementException:
        comment = ""
    responding = tweet.find_element_by_xpath('.//div[2]div[2]/div[2]').text
    tweet_body = comment + responding

    # reply count
    reply_cnt = tweet = driver.find_element_by_xpath('//div[@data-testid="reply"]')
    # retweet
    retweet_cnt = tweet = driver.find_element_by_xpath('//div[@data-testid="retweet"]')
    # likes
    like_cnt = tweet = driver.find_element_by_xpath('//div[@data-testid="like"]')

    tweet = (username, handle, postdate, tweet_body, reply_cnt, retweet_cnt, like_cnt)
    return tweet

tweet_data = []
for tweet in tweets:
    data = get_tweet_data(tweet)
    if data:
        tweet_data.append(data)