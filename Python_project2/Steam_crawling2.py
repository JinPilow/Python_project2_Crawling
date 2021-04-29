from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from multiprocessing import Pool, Manager

count = 0
tags = {}


def get_href():
    hrefs = soup.select("#search_resultsRows > a")
    data = []
    for href in hrefs:
        data.append(href.attrs['href'])
    return data


# 게임 주소 가져오고 들어가서 카테고리 가져오기
def get_content(href):
    global count
    global tags
    response = urlopen(href)
    soup = BeautifulSoup(response, 'html.parser')
    result2 = soup.select("a.app_tag")
    i = 0
    for j in result2:
        if j.get_text(" ", strip=True) in tags:
            tags[j.get_text(" ", strip=True)] = tags[j.get_text(" ", strip=True)] + 1
        else:
            tags[j.get_text(" ", strip=True)] = 1
        i = i + 1
        if i == 3:
            break
    count = count + 1
    print("processing...")


if __name__ == '__main__':
    start = time.time()

    response = urlopen('https://store.steampowered.com/search/?sort_by=_ASC&os=win&filter=globaltopsellers')
    soup = BeautifulSoup(response, 'html.parser')

    title = []

    # 게임 이름 가져오기
    result = soup.select("span.title")
    for i in result:
        title.append(i.get_text())

    pool = Pool(processes=16)
    pool.map(get_content, get_href())

    print(count)
    print(tags)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
