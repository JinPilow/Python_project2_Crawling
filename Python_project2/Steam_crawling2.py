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
        temp = temp.replace(",", "")
        temp = temp.split(' ')
        if len(temp) > 1:
            tlist[j]["price"] = temp[0]
            tlist[j]["discounted"] = temp[1]
        else:
            tlist[j]["price"] = temp[0]
        j = j + 1

    # tlist = {'RPG': 1, 'Action': 1, 'Story Rich': 1, 'title': 'Mass Effect™ Legendary Edition', 'price': '66000'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village', 'price': '66800'}, {'Strategy': 1, 'Historical': 1, 'War': 1, 'title': 'Total War: THREE KINGDOMS', 'price': '59800', 'discounted': '29900'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village & Resident Evil 7 Complete Bundle', 'price': '89000'}, {'title': 'Mass Effect™ Legendary Edition – ME3 Owner Offer', 'price': '82170'}, {'Open World Survival Craft': 1, 'Sandbox': 1, 'Survival': 1, 'title': 'Terraria', 'price': '10500', 'discounted': '5250'}, {'Co-op': 1, 'Multiplayer': 1, 'Class-Based': 1, 'title': 'Deep Rock Galactic', 'price': '31000', 'discounted': '18600'}, {'Open World Survival Craft': 1, 'Survival': 1, 'Underwater': 1, 'title': 'Subnautica: Below Zero', 'price': '31000'}, {'Open World': 1, 'Action': 1, 'RPG': 1, 'title': 'BIOMUTANT', 'price': '64900'}, {'Co-op': 1, 'Adventure': 1, 'Split Screen': 1, 'title': 'It Takes Two', 'price': '44000'}, {'Colony Sim': 1, 'Resource Management': 1, 'Post-apocalyptic': 1, 'title': 'Before We Leave', 'price': '20500', 'discounted': '15370'}, {'title': 'Destiny 2: Legendary Edition', 'price': '97500', 'discounted': '58500'}, {'Sexual Content': 1, 'Mature': 1, 'title': 'Grand Theft Auto V: Premium Edition', 'price': '33000'}, {'Open World Survival Craft': 1, 'Online Co-Op': 1, 'Survival': 1, 'title': 'Valheim', 'price': '20500'}, {'Action': 1, 'FPS': 1, 'Great Soundtrack': 1, 'title': 'DOOM Eternal Deluxe Edition', 'price': '100850', 'discounted': '33280'}, {'title': 'Middle-earth: Shadow of War Definitive Edition', 'price': '61000', 'discounted': '12200'}, {'Gore': 1, 'Violent': 1, 'Sexual Content': 1, 'title': 'Resident Evil Village Deluxe Edition', 'price': '79670'}, {'Action': 1, 'Adventure': 1, 'RPG': 1, 'title': 'Hood: Outlaws & Legends', 'price': '29800'}, {'title': 'Hood: Outlaws & Legends - Year 1 Edition', 'price': '49800'}, {'Survival': 1, 'Crafting': 1, 'Multiplayer': 1, 'title': 'Rust', 'price': '41000'}, {'Open World': 1, 'RPG': 1, 'Adventure': 1, 'title': 'The Elder Scrolls V: Skyrim Special Edition', 'price': '46160', 'discounted': '23080'}, {'Horror': 1, 'Online Co-Op': 1, 'Multiplayer': 1, 'title': 'Phasmophobia', 'price': '14500'}, {'Horror': 1, 'Online Co-Op': 1, 'Multiplayer': 1, 'title': 'Phasmophobia', 'price': '14500'}, {'Adventure': 1, 'Multiplayer': 1, 'Open World': 1, 'title': 'Sea of Thieves', 'price': '39400'}, {'Strategy': 1, 'Turn-Based Strategy': 1, 'Historical': 1, 'title': 'Total War™: ROME II - Emperor Edition', 'price': '59800', 'discounted': '14950'}, {'Strategy': 1, 'Action': 1, 'Grand Strategy': 1, 'title': 'Total War: WARHAMMER III', 'price': '60000'}, {'Multiplayer': 1, 'Online Co-Op': 1, 'Local Co-Op': 1, 'title': 'Overcooked! 2', 'price': '26000', 'discounted': '13000'}, {'Action': 1, 'FPS': 1, 'Great Soundtrack': 1, 'title': 'DOOM Eternal Standard Edition', 'price': '67000', 'discounted': '22110'}, {'Multiplayer': 1, 'FPS': 1, 'Zombies': 1, 'title': 'Call of Duty®: Black Ops III', 'price': '75700', 'discounted': '45420'}, {'Action': 1, 'World War II': 1, 'Shooter': 1, 'title': 'Hell Let Loose', 'price': '31000', 'discounted': '23250'}, {'Adventure': 1, 'Action': 1, 'Free to Play': 1, 'title': 'Destiny 2: Beyond Light + 1 Season', 'price': '56000', 'discounted': '37520'}, {'Simulation': 1, 'Strategy': 1, 'Action': 1, 'title': 'Arma 3 Creator DLC: S.O.G. Prairie Fire', 'price': '24500'}, {'Multiplayer': 1, 'FPS': 1, 'Zombies': 1, 'title': 'Call of Duty®: Black Ops III', 'price': '75700', 'discounted': '45420'}, {'Metroidvania': 1, 'Souls-like': 1, 'Gore': 1, 'title': 'Blasphemous', 'price': '26000', 'discounted': '10400'}, {'Racing': 1, 'Open World': 1, 'Driving': 1, 'title': 'Forza Horizon 4', 'price': '59900'}, {'Early Access': 1, 'RPG': 1, 'Dungeons & Dragons': 1, 'title': "Baldur's Gate 3", 'price': '66000'}, {'Flight': 1, 'Action': 1, 'Indie': 1, 'title': 'Project Wingman', 'price': '26000', 'discounted': '19500'}, {'Action': 1, 'Metroidvania': 1, 'Anime': 1, 'title': 'Lost Ruins', 'price': '20500'}, {'Action': 1, 'Adventure': 1, 'Free to Play': 1, 'title': 'Destiny 2: Season of the Splicer Silver Bundle', 'price': '18000'}, {'Destruction': 1, 'Physics': 1, 'Sandbox': 1, 'title': 'Teardown', 'price': '22500', 'discounted': '18000'}, {'title': 'Fallout 4: Game of the Year Edition', 'price': '69000', 'discounted': '34500'}, {'title': 'The Binding of Isaac: Rebirth Complete Bundle', 'price': '53000'}, {'Cyberpunk': 1, 'Open World': 1, 'RPG': 1, 'title': 'Cyberpunk 2077', 'price': '66000'}, {'Open World': 1, 'Adventure': 1, 'Story Rich': 1, 'title': 'Red Dead Redemption 2', 'price': '66000'}, {'Action': 1, 'Adventure': 1, 'Free to Play': 1, 'title': 'Destiny 2: Beyond Light Deluxe Edition', 'price': '78500', 'discounted': '58870'}, {'Action': 1, 'Adventure': 1, 'Free to Play': 1, 'title': 'Apex Legends™ - Legacy Pack', 'price': '5600'}, {'Open World': 1, 'Post-apocalyptic': 1, 'Action': 1, 'title': 'Days Gone', 'price': '58800'}, {'Mature': 1, 'Utilities': 1, 'Software': 1, 'title': 'Wallpaper Engine', 'price': '4400'}, {'RPG': 1, 'Action': 1, 'Co-op': 1, 'title': 'OUTRIDERS', 'price': '70920'}, {'title': 'EA Play', 'price': '5000'}
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

    total_price = dict(sorted(total_price.items(), reverse=True))
    print(total_price)

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
