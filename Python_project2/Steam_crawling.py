from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
url = "https://store.steampowered.com/search/?filter=topsellers"
driver.get(url)

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

#time.sleep(3)
driver.quit()