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

    # 각 게임 주소에 접속한다
    response = urlopen(href)
    soup = BeautifulSoup(response, 'html.parser')

    # 게임 타이틀 가져오기
    title = soup.select("div.details_block > b:nth-child(1)")
    if title:
        cont['title'] = str(title[0].find_next_siblings(text=True)[0])

    price = soup.select("div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > "
                        "div.game_purchase_price.price")
    if not price:
        price = soup.select("div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > "
                            "div.discount_block.game_purchase_discount > div.discount_prices > "
                            "div.discount_original_price")
    print(cont['title'])
    for text in price:
        print(text.get_text(" ", strip=True))
    print(type(price))

    # 태그들을 가져온다 (3개만)
    result2 = soup.select("a.app_tag")
    i = 0
    temp = {}
    for content in result2:
        temp[content.get_text(" ", strip=True)] = 1
        i = i + 1
        if i == 3:
            break
    cont['tags'] = temp

    print("processing...")

    return cont


if __name__ == '__main__':
    start = time.time()

    # GLOBAL TOP SELLERS 사이트
    response = urlopen('https://store.steampowered.com/search/?sort_by=_ASC&os=win&filter=globaltopsellers')
    soup = BeautifulSoup(response, 'html.parser')

    # 각 게임 태그 가져오기 (멀티프로세싱으로 속도 개선)
    pool = Pool(processes=16)
    tlist = pool.map(get_content, get_href())

    # # 게임 이름 가져오기
    # result = soup.select("span.title")
    # j = 0
    # for i in result:
    #     tlist[j]["title"] = i.get_text()
    #     j = j + 1

    # 게임 가격 가져오기
    result2 = soup.select("div.col.search_price.responsive_secondrow")
    j = 0
    for i in result2:
        temp = i.get_text(" ", strip=True).replace("₩ ", "")
        temp = temp.replace(",", "")
        temp = temp.split(' ')
        if len(temp) > 1:
            tlist[j]["price"] = temp[0]
            tlist[j]["discounted"] = temp[1]
        else:
            tlist[j]["price"] = temp[0]
        j = j + 1

    # tlist = {'tags': {'Open World': 1, 'Action': 1, 'RPG': 1}, 'title': 'BIOMUTANT', 'price': '64900'}, {'tags': {'RPG': 1, 'Story Rich': 1, 'Action': 1}, 'title': 'Mass Effect™ Legendary Edition', 'price': '66000'}, {'tags': {'Dark Humor': 1, 'Nature': 1, 'Underwater': 1}, 'title': 'Maneater', 'price': '41000', 'discounted': '34850'}, {'tags': {'Open World': 1, 'Post-apocalyptic': 1, 'Singleplayer': 1}, 'title': 'Days Gone', 'price': '58800'}, {'tags': {'Gore': 1, 'Violent': 1, 'Sexual Content': 1}, 'title': 'Resident Evil Village', 'price': '66800'}, {'tags': {'Multiplayer': 1, 'Sports': 1, 'Team-Based': 1}, 'title': 'Knockout City™', 'price': '22000'}, {'tags': {}, 'title': 'The Witcher 3: Wild Hunt - Game of the Year Edition', 'price': '54800', 'discounted': '10960'}, {'tags': {'Open World Survival Craft': 1, 'Survival': 1, 'Underwater': 1}, 'title': 'Subnautica: Below Zero', 'price': '31000'}, {'tags': {'Co-op': 1, 'Adventure': 1, 'Split Screen': 1}, 'title': 'It Takes Two', 'price': '44000'}, {'tags': {'Open World': 1, 'Adventure': 1, 'Story Rich': 1}, 'title': 'Red Dead Redemption 2', 'price': '66000', 'discounted': '44220'}, {'tags': {'Action': 1, 'Adventure': 1, 'Female Protagonist': 1}, 'title': 'Control Ultimate Edition', 'price': '45000', 'discounted': '18000'}, {'tags': {'Sexual Content': 1, 'Mature': 1}, 'title': 'Grand Theft Auto V: Premium Edition', 'price': '33000'}, {'tags': {'Adventure': 1, 'Action': 1, 'Open World': 1}, 'title': 'Generation Zero®', 'price': '26000', 'discounted': '7280'}, {'tags': {'JRPG': 1, 'RPG': 1, 'Creature Collector': 1}, 'title': 'Shin Megami Tensei III Nocturne HD Remaster', 'price': '49800'}, {'tags': {'Open World Survival Craft': 1, 'Survival': 1, 'Online Co-Op': 1}, 'title': 'Valheim', 'price': '20500'}, {'tags': {'Survival': 1, 'Crafting': 1, 'Multiplayer': 1}, 'title': 'Rust', 'price': '41000'}, {'tags': {'Survival': 1, 'Crafting': 1, 'Multiplayer': 1}, 'title': 'Rust', 'price': '41000'}, {'tags': {}, 'title': 'Generation Zero® - Resistance Bundle', 'price': '43000', 'discounted': '15580'}, {'tags': {'Cyberpunk': 1, 'Open World': 1, 'RPG': 1}, 'title': 'Cyberpunk 2077', 'price': '66000', 'discounted': '52800'}, {'tags': {'Horror': 1, 'Online Co-Op': 1, 'Multiplayer': 1}, 'title': 'Phasmophobia', 'price': '14500'}, {'tags': {}, 'title': 'Borderlands 3: Super Deluxe Edition', 'price': '88900', 'discounted': '40000'}, {'tags': {'Adventure': 1, 'Multiplayer': 1, 'Open World': 1}, 'title': 'Sea of Thieves', 'price': '39400'}, {'tags': {'Gore': 1, 'Violent': 1}, 'title': 'Warframe Gara Prime Access: Mass Vitrify Bundle', 'price': '142000'}, {'tags': {'Cyberpunk': 1, 'Sci-fi': 1, 'Atmospheric': 1}, 'title': 'Cloudpunk', 'price': '20500', 'discounted': '10250'}, {'tags': {'Gore': 1, 'Violent': 1, 'Sexual Content': 1}, 'title': 'Resident Evil Village & Resident Evil 7 Complete Bundle', 'price': '89000'}, {'tags': {'Multiplayer': 1, 'Hunting': 1, 'Online Co-Op': 1}, 'title': 'Hunt: Showdown', 'price': '49000', 'discounted': '24500'}, {'tags': {'Open World Survival Craft': 1, 'Survival': 1, 'Open World': 1}, 'title': 'Subnautica', 'price': '31000'}, {'tags': {'Choices Matter': 1, 'Story Rich': 1, 'Multiple Endings': 1}, 'title': 'Detroit: Become Human', 'price': '39900', 'discounted': '27930'}, {'tags': {'Mature': 1, 'Utilities': 1, 'Software': 1}, 'title': 'Wallpaper Engine', 'price': '4400'}, {'tags': {'Action': 1, 'Adventure': 1, 'Free to Play': 1}, 'title': 'Destiny 2: Throne of Atheon Emote Bundle', 'price': '18000'}, {'tags': {}, 'title': 'EA Play', 'price': '5000'}, {'tags': {'Horror': 1, 'Survival Horror': 1, 'Multiplayer': 1}, 'title': 'Dead by Daylight', 'price': '21000'}, {'tags': {'Racing': 1, 'Open World': 1, 'Driving': 1}, 'title': 'Forza Horizon 4', 'price': '59900'}, {'tags': {'Sports': 1, 'Soccer': 1, 'PvP': 1}, 'title': 'EA SPORTS™ FIFA 21', 'price': '88000', 'discounted': '22000'}, {'tags': {'Survival': 1, 'Shooter': 1, 'Multiplayer': 1}, 'title': "PLAYERUNKNOWN'S BATTLEGROUNDS", 'price': '32000'}, {'tags': {'Action': 1, 'Shooter': 1, 'FPS': 1}, 'title': 'Zero Hour', 'price': '12500', 'discounted': '6250'}, {'tags': {'Farming Sim': 1, 'Life Sim': 1, 'RPG': 1}, 'title': 'Stardew Valley', 'price': '16000'}, {'tags': {}, 'title': "Sid Meier's Civilization VI : Platinum Edition", 'price': '181500', 'discounted': '54800'}, {'tags': {'Early Access': 1, 'RPG': 1, 'Dungeons & Dragons': 1}, 'title': "Baldur's Gate 3", 'price': '66000'}, {'tags': {'RPG': 1, 'Action': 1, 'Looter Shooter': 1}, 'title': 'OUTRIDERS', 'price': '70920', 'discounted': '53190'}, {'tags': {'Exploration': 1, 'Space': 1, 'Adventure': 1}, 'title': 'Outer Wilds', 'price': '26000', 'discounted': '15600'}, {'tags': {'Survival': 1, 'Open World Survival Craft': 1, 'Multiplayer': 1}, 'title': 'Raft', 'price': '21000'}, {'tags': {}, 'title': 'The Binding of Isaac: Rebirth Complete Bundle', 'price': '53000'}, {'tags': {'Violent': 1, 'Gore': 1}, 'title': 'Shadow of the Tomb Raider: Definitive Edition', 'price': '100500', 'discounted': '14740'}, {'tags': {}, 'title': 'Destiny 2: Legendary Edition', 'price': '97500'}, {'tags': {'Open World Survival Craft': 1, 'Sandbox': 1, 'Survival': 1}, 'title': 'Terraria', 'price': '10500'}, {'tags': {'Adventure': 1, 'Action': 1, 'Female Protagonist': 1}, 'title': 'Rise of the Tomb Raider™', 'price': '59900', 'discounted': '11980'}, {'tags': {}, 'title': 'Control Ultimate Edition + Alan Wake Franchise Bundle', 'price': '80500', 'discounted': '22830'}, {'tags': {'Strategy': 1, 'Turn-Based Strategy': 1, 'Historical': 1}, 'title': 'Sid Meier’s Civilization® VI', 'price': '65000', 'discounted': '16250'}, {'tags': {'Open World Survival Craft': 1, 'Survival': 1, 'Open World': 1}, 'title': 'ARK: Survival Evolved', 'price': '51000'}# 크롤링 끝
    print("크롤링 갯수 :{}".format(len(tlist)))
    print("크롤링 시간 :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    print(tlist)

    # 태그 개수 통계
    total_tag = {}
    for i in tlist:
        for tag in list(i['tags'].keys()):
            if tag in total_tag:
                total_tag[tag] = total_tag[tag] + 1
            else:
                total_tag[tag] = 1

    # 가격별 통계
    total_price = {}
    for i in tlist:
        price = int(i['price'])
        if price < 10000:
            name = "1만원 이하"
            if "1만원 이하" in total_price:
                total_price["1만원 이하"] = total_price["1만원 이하"] + 1
            else:
                total_price["1만원 이하"] = 1

        elif price >= 70000:
            name = "7만원 이상"
            if "7만원 이상" in total_price:
                total_price["7만원 이상"] = total_price["7만원 이상"] + 1
            else:
                total_price["7만원 이상"] = 1

        else:
            for j in range(1, 7):
                name = str(j)+"만원대"
                if 10000*(j+1) > price >= 10000*j:
                    if name in total_price:
                        total_price[name] = total_price[name] + 1
                        break
                    else:
                        total_price[name] = 1
                        break

    # 가격별 결과 정렬
    total_price = dict(sorted(total_price.items(), reverse=True))
    # print(total_price)


    # 그래프 출력
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.barh(list(total_tag.keys()), total_tag.values())
    plt.title('태크별')
    plt.ylabel('Tags')
    fig.set_tight_layout(True)

    fig, ax = plt.subplots()
    plt.bar(list(total_price.keys()), total_price.values())
    plt.title('가격별')

    fig.set_tight_layout(True)
    plt.show()
