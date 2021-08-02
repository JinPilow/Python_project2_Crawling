from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument("window-size=1366x768")
chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36")


# chrome_options = Options()
# chrome_options.add_argument("--headless")

browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(6)

url = "https://store.steampowered.com/search/?filter=topsellers"
browser.get(url)

soup = BeautifulSoup(browser.page_source, "lxml")

games = soup.find("div", attrs={"id":"search_resultsRows"}).find_all("a")

for idx, game in enumerate(games):
    title = game.find("span", attrs={"class":"title"}).get_text()

    discount_price = game.find("div", attrs={"class":"col search_price discounted responsive_secondrow"})
    if discount_price:
        price = game.find("div", attrs={"class": "col search_price discounted responsive_secondrow"}).span.get_text().strip()
    else:
        price = game.find("div", attrs={"class": "col search_price_discount_combined responsive_secondrow"}).get_text().strip()


    print(f"{idx}. {title}\n가격:{price}")

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

# from bs4 import BeautifulSoup
# from multiprocessing import Pool, Manager
# import time
# import requests
# import re
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import pandas as pd
# from pandas import DataFrame
#
# def get_url():
#     site = soup.find_all('a', href=re.compile('https://store.steampowered.com/' + \
#                                                     'app/|bundle/|sub/'))
#     url = []
#     for i in site:
#         url.append(i.get('href'))
#     return url
#
# # url에 접속해 장르를 가져오는 함수
# def get_info(url):
#     cont = {}
#     html = requests.get(url)
#     soup = BeautifulSoup(html.content, 'html.parser')
#     genres = soup.find_all('a', href= re.compile('https://store.steampowered.com/genre/'))
#     genre = []
#     for category in genres[2:]:
#         genre.append(category.get_text().strip())
#
#     title = soup.select_one('div.details_block > b')
#     # print(title.find_next_siblings(text=True)[0])
#     if title:
#         print(title.find_next_siblings(text=True)[0])
#     else:
#         return
#
#     # price = soup.select_one('div.game_purchase_price.price')
#     # print(price)
#
#
#
# # 가격에서 콤마를 없애고 정수형으로 만드는 함수
# def comma_to_int(string):
#     number = re.sub(",", "", string)
#     return int(number)
#
#
#
# if __name__ == '__main__':
#     start_time = time.time()
#     html = requests.get('https://store.steampowered.com/search/?filter=topsellers')
#     soup = BeautifulSoup(html.content, 'html.parser')
#
#     price = soup.select('div.col.search_price')
#
#     start_time = time.time()
#     pool = Pool(processes = 16)
#     pool.map(get_info, get_url())
#     print("실행 시간 : %s초" % (time.time() - start_time))
#
#     # list_title = [i.get_text() for i in title]
#     list_genre = []
#     list_price = []
#
#
#     # 리스트에 가격 저장
#     for i in price:
#         if i.get_text().strip().count("₩") == 1:
#             a = comma_to_int(i.get_text().strip().replace("₩", "").strip())
#             list_price.append(a)
#         else:
#             s = i.get_text().strip().split("₩")
#             a = comma_to_int(s[1].strip())
#             list_price.append(a)

    # title_price = dict(zip(list_title, list_price))
#
# # 시각화
# sns.barplot(x=list_title,y=list_price)
# plt.xticks(rotation = 90, fontsize = 6)
# plt.show()
#
# # 데이터프레임화
# # df = DataFrame({'TITLE': list_title, 'PRICE': list_price})
# df = DataFrame(list_title, list_price, list_genre)
# print(df)
#
# factor_price = pd.cut(df.col_2, 4)
# group_price = df.col_2.groupby(factor_price)
# print(group_price.agg(['count', 'mean', 'std', 'min', 'max']))
