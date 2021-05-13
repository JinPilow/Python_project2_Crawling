from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, Manager
import matplotlib.ticker as ticker


# 각 게임 페이지 주소 가져오기
def get_href():
    # 클릭 대상의 a태그 옵션들을 가져온다
    hrefs = soup.select("#search_resultsRows > a")
    data = []
    for href in hrefs:
        # href 내용물을 가져온다
        data.append(href.attrs['href'])
    return data


# 게임 주소 가져오고 들어가서 카테고리 가져오기
def get_content(href):
    cont = {}

    response = urlopen(href)
    soup = BeautifulSoup(response, 'html.parser')

    # 태그들을 가져온다 (3개만)
    result2 = soup.select("a.app_tag")
    i = 0
    for content in result2:
        cont[content.get_text(" ", strip=True)] = 1
        i = i + 1
        if i == 3:
            break

    print("processing...")

    return cont


if __name__ == '__main__':
    start = time.time()

    response = urlopen('https://store.steampowered.com/search/?sort_by=_ASC&os=win&filter=globaltopsellers')
    soup = BeautifulSoup(response, 'html.parser')

    # 각 게임 태그 가져오기 (멀티프로세싱으로 속도 개선)
    pool = Pool(processes=16)
    tlist = pool.map(get_content, get_href())

    # 게임 이름 가져오기
    result = soup.select("span.title")
    j = 0
    for i in result:
        tlist[j]["title"] = i.get_text()
        j = j + 1

    # 게임 가격 가져오기
    result2 = soup.select("div.col.search_price.responsive_secondrow")
    j = 0
    for i in result2:
        temp = i.get_text(" ", strip=True).replace("₩ ", "")
        temp = temp.split('  ')
        if len(temp) > 1:
            tlist[j]["price"] = temp[0]
            tlist[j]["discounted"] = temp[1]
        else:
            tlist[j]["price"] = temp[0]
        j = j + 1

    print("크롤링 갯수 :{}".format(len(result)))
    print("크롤링 시간 :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

    # 태그 개수 통계
    total_tag = {}
    for i in tlist:
        for tag in list(i.keys()):
            if tag in total_tag:
                total_tag[tag] = total_tag[tag] + 1
            else:
                total_tag[tag] = 1

    # 제목 갯수는 삭제
    del total_tag['title']
    del total_tag['price']

    # print(total_tag)

    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    fig.set_tight_layout(True)
    plt.barh(list(total_tag.keys()), total_tag.values())
    plt.ylabel('Tags')
    plt.show()
