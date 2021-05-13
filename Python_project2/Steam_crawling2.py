import math

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

    tlist = {'RPG': 1, 'Action': 1, 'Story Rich': 1, 'title': 'Mass Effect™ Legendary Edition', 'price': '66,000'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village', 'price': '66,800'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village & Resident Evil 7 Complete Bundle', 'price': '89,000'}, {'Co-op': 1, 'Adventure': 1, 'Split Screen': 1, 'title': 'It Takes Two', 'price': '44,000'}, {'Open World': 1, 'Action': 1, 'RPG': 1, 'title': 'BIOMUTANT', 'price': '64,900'}, {'Action': 1, 'Adventure': 1, 'RPG': 1, 'title': 'Hood: Outlaws & Legends', 'price': '29,800'}, {'title': 'Hood: Outlaws & Legends - Year 1 Edition', 'price': '49,800'}, {'title': 'Destiny 2: Legendary Edition', 'price': '97,500 58,500'}, {'Action': 1, 'FPS': 1, 'Great Soundtrack': 1, 'title': 'DOOM Eternal Deluxe Edition', 'price': '100,850 33,280'}, {'Sexual Content': 1, 'Mature': 1, 'title': 'Grand Theft Auto V: Premium Edition', 'price': '33,000'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village Deluxe Edition', 'price': '79,670'}, {'Open World Survival Craft': 1, 'Online Co-Op': 1, 'Survival': 1, 'title': 'Valheim', 'price': '20,500'}, {'Open World': 1, 'RPG': 1, 'Adventure': 1, 'title': 'The Elder Scrolls V: Skyrim Special Edition', 'price': '46,160 23,080'}, {'title': 'Mass Effect™ Legendary Edition – ME3 Owner Offer', 'price': '82,170'}, {'Action': 1, 'Adventure': 1, 'Free to Play': 1, 'title': 'Destiny 2: Season of the Splicer Silver Bundle', 'price': '18,000'}, {'Horror': 1, 'Online Co-Op': 1, 'Multiplayer': 1, 'title': 'Phasmophobia', 'price': '14,500'}, {'Simulation': 1, 'Strategy': 1, 'Action': 1, 'title': 'Arma 3 Creator DLC: S.O.G. Prairie Fire', 'price': '24,500 20,820'}, {'Survival': 1, 'Crafting': 1, 'Multiplayer': 1, 'title': 'Rust', 'price': '41,000'}, {'Open World Survival Craft': 1, 'Survival': 1, 'Underwater': 1, 'title': 'Subnautica: Below Zero', 'price': '31,000'}, {'Adventure': 1, 'Action': 1, 'Free to Play': 1, 'title': 'Destiny 2: Beyond Light + 1 Season', 'price': '56,000 37,520'}, {'Destruction': 1, 'Physics': 1, 'Sandbox': 1, 'title': 'Teardown', 'price': '22,500 18,000'}, {'Action': 1, 'FPS': 1, 'Great Soundtrack': 1, 'title': 'DOOM Eternal Standard Edition', 'price': '67,000 22,110'}, {'title': 'Arma 3 Ultimate Edition', 'price': '158,800 43,120'}, {'Adventure': 1, 'Multiplayer': 1, 'Open World': 1, 'title': 'Sea of Thieves', 'price': '39,400'}, {'title': 'Journey to the Savage Planet Deluxe Edition', 'price': '39,000 18,270'}, {'Multiplayer': 1, 'FPS': 1, 'Zombies': 1, 'title': 'Call of Duty®: Black Ops III', 'price': '75,700 45,420'}, {'title': 'Outward & Pathfinder Ultimate Bundle', 'price': '135,000 38,910'}, {'Action': 1, 'Multiplayer': 1, 'Military': 1, 'title': 'Arma 3', 'price': '36,000 9,000'}, {'Multiplayer': 1, 'FPS': 1, 'Zombies': 1, 'title': 'Call of Duty®: Black Ops III', 'price': '75,700 45,420'}, {'Adventure': 1, 'Action': 1, 'Action-Adventure': 1, 'title': 'Journey To The Savage Planet', 'price': '31,000 15,500'}, {'Action': 1, 'Adventure': 1, 'Free to Play': 1, 'title': 'Destiny 2: Beyond Light Deluxe Edition', 'price': '78,500 58,870'}, {'title': 'Fallout 4: Game of the Year Edition', 'price': '69,000 34,500'}, {'title': 'Pathfinder: Kingmaker - Imperial Edition Bundle', 'price': '49,500 21,830'}, {'Racing': 1, 'Open World': 1, 'Driving': 1, 'title': 'Forza Horizon 4', 'price': '59,900'}, {'Survival': 1, 'Shooter': 1, 'Multiplayer': 1, 'title': "PLAYERUNKNOWN'S BATTLEGROUNDS", 'price': '32,000'}, {'Mature': 1, 'Utilities': 1, 'Software': 1, 'title': 'Wallpaper Engine', 'price': '4,400'}, {'title': 'The Binding of Isaac: Rebirth Complete Bundle', 'price': '53,000'}, {'Early Access': 1, 'RPG': 1, 'Dungeons & Dragons': 1, 'title': "Baldur's Gate 3", 'price': '66,000'}, {'Farming Sim': 1, 'Life Sim': 1, 'RPG': 1, 'title': 'Stardew Valley', 'price': '16,000'}, {'Open World': 1, 'Adventure': 1, 'Story Rich': 1, 'title': 'Red Dead Redemption 2', 'price': '66,000'}, {'RPG': 1, 'Open World': 1, 'Survival': 1, 'title': 'Outward', 'price': '41,000 12,300'}, {'Open World Survival Craft': 1, 'Survival': 1, 'Open World': 1, 'title': 'The Forest', 'price': '20,500'}, {'Action': 1, 'Adventure': 1, 'Battle Royale': 1, 'title': 'Apex Legends™ - Champion Edition', 'price': '44,000'}, {'title': 'EA Play', 'price': '5,000'}, {'Survival': 1, 'Open World Survival Craft': 1, 'Multiplayer': 1, 'title': 'Raft', 'price': '21,000'}, {'Great Soundtrack': 1, 'Story Rich': 1, 'Action': 1, 'title': 'NieR Replicant™ ver.1.22474487139...', 'price': '69,800'}, {'Cyberpunk': 1, 'Open World': 1, 'RPG': 1, 'title': 'Cyberpunk 2077', 'price': '66,000'}, {'Funny': 1, 'Physics': 1, 'Multiplayer': 1, 'title': 'Gang Beasts', 'price': '21,000 9,450'}, {'RPG': 1, 'Action': 1, 'Co-op': 1, 'title': 'OUTRIDERS', 'price': '70,920'}, {'Early Access': 1, 'Online Co-Op': 1, 'Horror': 1, 'title': 'GTFO', 'price': '45,000 36,000'}

    print("크롤링 갯수 :{}".format(len(tlist)))
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

    # total_price = {}
    # for i in tlist:
    #     price = math.floor(int(i['price']))
    #     print(price)

    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.barh(list(total_tag.keys()), total_tag.values())
    plt.title('태크별 게임')
    plt.ylabel('Tags')

    fig.set_tight_layout(True)
    plt.show()
