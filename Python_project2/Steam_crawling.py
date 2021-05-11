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