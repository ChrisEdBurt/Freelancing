import re
import csv
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

USER = '****'
MY_PASSWORD = '****'


def get_tweet_data(card):
    """Extract data from tweet card"""
    username = card.find_element_by_xpath('.//span').text
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NoSuchElementException:
        return
    
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    tweet = (username, handle, postdate, text, reply_cnt, retweet_cnt, like_cnt)
    return tweet

search_term = input('search term: ')
search_input_str = str(search_term)

options = Options()
options.add_argument("window-size=1280,1000")
driver = webdriver.Chrome(chrome_options=options)

# navigate to login screen
driver.get('https://www.twitter.com/login')

# input username and password 
sleep(1)
username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(USER)
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(MY_PASSWORD)
password.send_keys(Keys.RETURN) 
sleep(1)

try:
    # Getting current URL
    get_url = driver.current_url
    acc_check_url = "https://twitter.com/login?email_disabled=true&redirect_after_login=%2F"
    if acc_check_url in get_url:
        username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        username.send_keys('JimmyJimJan1')
        password = driver.find_element_by_xpath('//input[@name="session[password]"]')
        password.send_keys('Password!')
        password.send_keys(Keys.RETURN)
except:
    "No Account Check"

sleep(1)
# find search input and search for term
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys(search_term)
search_input.send_keys(Keys.RETURN)
sleep(1)

# navigate to historical 'latest' tab
driver.find_element_by_link_text('Latest').click()

# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards:
    # for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    scroll_attempt = 0
    
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                print("")
                print(f"Scraping of " + search_input_str + " has been completed")
                break
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()
results_filename = search_input_str + '.csv'
print("Writing tweet results to " + search_input_str)

if len(data) != 0:
    # Saving the tweet data
    with open(results_filename, 'a', newline='', encoding='utf-8') as f:
        header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Comments', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print("Writing tweet results to csv")
    
else:
    print("There were no tweets found using that " + search_input_str + "please try again with a different search term.")