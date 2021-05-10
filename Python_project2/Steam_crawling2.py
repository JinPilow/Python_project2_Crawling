from bs4 import BeautifulSoup
from urllib.request import urlopen
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool, Manager


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

    print("크롤링 갯수 :{}".format(len(result)))

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

    print(total_tag)

    # myList = total_tag.items()
    # myList = sorted(total_tag)
    # x, y = zip(*myList)

    plt.bar(list(total_tag.keys()), total_tag.values())
    plt.show()

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
