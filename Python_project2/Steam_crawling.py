from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
url = "https://store.steampowered.com/search/?filter=topsellers"
driver.get(url)

dic = dict()
i = 1
while i <= 100:
    try:
        link = driver.find_element_by_css_selector('#search_resultsRows > a:nth-child(' + str(i) + ')')
        link.click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('div', class_='apphub_AppName')
        tag = soup.find_all('a', class_='app_tag')
        title = title.get_text().strip()
        li = []
        for category in tag[:3]:
            li.append(category.get_text().strip())
        dic.setdefault(title, li)
        driver.back()
    except:
        #if 'https://store.steampowered.com/agecheck/app/' in html:
        print("여기")
        link = driver.find_element_by_css_selector('#ageYear > option:nth-child(96)')
        link.click()
        link = driver.find_element_by_css_selector('#app_agegate > div.main_content_ctn > div.agegate_text_container.btns > a:nth-child(1)')
        link.click()
    finally:
        i += 1
print(dic)

#time.sleep(3)
driver.quit()