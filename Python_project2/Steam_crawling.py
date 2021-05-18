'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(6)

driver = webdriver.Chrome()
url = "https://store.steampowered.com/search/?filter=topsellers"
driver.get(url)

'''
'''
dic = dict()
i = 1
while i <= 2:
    link = driver.find_element_by_css_selector('#search_resultsRows > a:nth-child(' + str(i) + ')')
    link.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if str(soup.select_one('.apphub_AppName')) == "None":
            title = soup.select_one('.pageheader')
        else:
            title = soup.select_one('.apphub_AppName')
        tag = soup.find_all('a', class_='app_tag')
        print(title.get_text())
        li = []
        for category in tag[:3]:
            li.append(category.get_text().strip())
        dic.setdefault(title, li)
    except:
        #if 'https://store.steampowered.com/agecheck/app/' in html:
        link = driver.find_element_by_css_selector('#ageYear > option:nth-child(96)')
        link.click()
        link = driver.find_element_by_css_selector('#app_agegate > div.main_content_ctn > div.agegate_text_container.btns > a:nth-child(1)')
        link.click()
        if str(soup.select_one('.apphub_AppName')) == "None":
            title = soup.select_one('.pageheader')
        else:
            title = soup.select_one('.apphub_AppName')
        tag = soup.find_all('a', class_='app_tag')
        li = []
        for category in tag[:3]:
            li.append(category.get_text().strip())
        dic.setdefault(title, li)
    finally:
        i += 1
        driver.back()
print(dic)
'''
# time.sleep(3)
# driver.quit()
'''
dic = dict()
i = 2
while i <= 2:
    link = driver.find_element_by_css_selector('#search_resultsRows > a:nth-child(' + str(i) + ')')
    link.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    contents = soup.select('div.page_content_ctn')
    for content in contents:
        if content.find('div', 'apphub_AppName') and content.find('a', 'app_tag'):
            title = content.select('div.apphub_AppName')

driver.quit()
'''

from bs4 import BeautifulSoup
import multiprocessing
import requests
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pandas import DataFrame



html = requests.get('https://store.steampowered.com/search/?filter=topsellers')
soup = BeautifulSoup(html.content, 'html.parser')

title = soup.select('span.title')
price = soup.select('div.col.search_price')
genre_site = soup.find_all('a', href = re.compile('https://store.steampowered.com/'+\
                                                'app/|bundle/|sub/'))
# url에 접속해 장르를 가져오는 함수
def get_genre(href):
    html = requests.get(href)
    soup = BeautifulSoup(html.content, 'html.parser')
    tags = soup.find_all('a', href= re.compile('https://store.steampowered.com/' + 'genre/'))
    genre = []
    for category in tags[2:]:
        genre.append(category.get_text().strip())
    return genre

# 가격에서 콤마를 없애고 정수형으로 만드는 함수
def comma_to_int(string):
    number = re.sub(",", "", string)
    return int(number)

list_title = [i.get_text() for i in title]
list_genre = []
list_price = []

# 리스트에 장르 저장
for i in genre_site:
    href = i.attrs['href']
    list_genre.append(get_genre(href))

# 리스트에 가격 저장
for i in price:
    if i.get_text().strip().count("₩") == 1:
        a = comma_to_int(i.get_text().strip().replace("₩", "").strip())
        list_price.append(a)
    else:
        s = i.get_text().strip().split("₩")
        a = comma_to_int(s[1].strip())
        list_price.append(a)

# title_price = dict(zip(list_title, list_price))

# 시각화
sns.barplot(x=list_title,y=list_price)
plt.xticks(rotation = 90, fontsize = 6)
plt.show()

# 데이터프레임화
# df = DataFrame({'col_1': list_title, 'col_2': list_price})
df = DataFrame(list_title, list_price, list_genre)
print(df)

factor_price = pd.cut(df.col_2, 4)
group_price = df.col_2.groupby(factor_price)
print(group_price.agg(['count', 'mean', 'std', 'min', 'max']))
