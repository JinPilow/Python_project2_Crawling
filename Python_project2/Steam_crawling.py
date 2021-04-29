from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
url = "https://store.steampowered.com/search/?filter=topsellers"
driver.get(url)

dic = dict()
for i in range(1,6):
    link = driver.find_element_by_css_selector('#search_resultsRows > a:nth-child(' + str(i) + ')')
    link.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_='apphub_AppName')
    tag = soup.find_all('a', class_='app_tag')
    title = title.get_text().strip()
    li = []
    for i in tag[:3]:
        li.append(i.get_text().strip())
    dic.setdefault(title, li)
    driver.back()
print(dic)

#time.sleep(3)
driver.quit()