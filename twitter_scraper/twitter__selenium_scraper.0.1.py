from logging import exception
import math
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
    
    # get a string of all emojis contained in the tweet
    emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    emoji_list = []
    for tag in emoji_tags:
        filename = tag.get_attribute('src')
        try:
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    
    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt)
    return tweet

print()
print('Input timeframe for the tweets that you wish to scrape.')
print('1 will scrape tweets up until 1 hour ago, then it will finish.')
tweet_time_period = int(input())
print('Scraping for ' + str(tweet_time_period) + " hour/s")
if input == '': 
    tweet_time_period = 5

search_term = '#Dog'
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
scroll_attempt = 0

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)

        cur_time = datetime.utcnow()
        tweet_time = tweet[2][:-5]
        pattern = r'[T]'
        tweet_time = re.sub(pattern, '', tweet_time)
        tweet_date = datetime.strptime(tweet_time, "%Y-%m-%d%H:%M:%S")
        time_dif = cur_time - tweet_date
        time_dif = round(float(time_dif.seconds / 60 / 60), 2)
        print("Differnce of : " + str(time_dif) + " hours")
        print("")
                
        if int(time_dif > tweet_time_period):
            print("")
            print("Tweet is out of requested time frame.")
            print("Scraping is complete.....")
            scrolling = False
            break

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
        header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    
else:
    print("There were no tweets found using that " + search_input_str + "please try again with a different search term.")