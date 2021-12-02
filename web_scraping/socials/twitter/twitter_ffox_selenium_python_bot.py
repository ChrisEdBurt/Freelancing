from os import link
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class TwitterBot:
    def __init__(self,username,password,phone_number):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(1)

        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_tweet(self,hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q=' + hashtag + '&src=typd')
        time.sleep(1)
        for i in range(1,3):
            bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(3)
            tweets = bot.find_elements_by_xpath('//div[@data-testid="tweet"]')
            print(tweets[0].get_attribute("innerText"))

twitter_bot = TwitterBot('fr33twitter@outlook.com','Password!','0274104689')
twitter_bot.login()
twitter_bot.like_tweet('webdevelopment')
