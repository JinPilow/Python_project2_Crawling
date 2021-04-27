from urllib.request import urlopen
from bs4 import BeautifulSoup
'''
html = urlopen("https://store.steampowered.com/search/?filter=topsellers")

soup = BeautifulSoup(html, 'html.parser')
title = soup.find_all(class_='title')
for i in title:
    print(i.text.strip())
'''
'''
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://store.steampowered.com/search/?filter=topsellers'

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)
print(driver.current_url)
driver.close()
driver.implicitly_wait(time_to_wait=5)
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(5)

driver.get(url='https://www.google.com/')

search_box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

search_box.send_keys('greeksharifa.github.io')
search_box.send_keys(Keys.RETURN)

elements = driver.find_elements_by_xpath('//*[@id="rso"]/div[*]/div/div[1]/a/h3/span')

for element in elements:
    print(element.text)
    print(element.text, file=open('gorio.txt', 'w', encoding='utf-8'))

sleep(3)
driver.close()