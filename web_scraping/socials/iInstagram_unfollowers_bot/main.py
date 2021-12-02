from logging import lastResort
from os import name, scandir
from selenium import webdriver
import time

option = webdriver.ChromeOptions()
option.add_argument("--start-maximized")
option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
 
USERNAME = '****'
PASSWORD = '****'

class InstagramBot:
    def __init__(self, USERNAME, PASSWORD):
        self.driver = webdriver.Chrome(options=option)
        self.username = USERNAME
        self.driver.get('http://www.instagram.com')
        time.sleep(3)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(PASSWORD)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        
    def get_unfollowers(self):
        
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        time.sleep(2)
        
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self.get_names()
        time.sleep(2)

        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self.get_names()
        time.sleep(2)

        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def get_names(self):
        time.sleep(1)
        scroll_box = self.driver.find_element_by_xpath('//div[@role="dialog"]')
        print(scroll_box)
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()

instaBot = InstagramBot(USERNAME, PASSWORD)
instaBot.get_unfollowers()