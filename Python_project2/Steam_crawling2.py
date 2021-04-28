from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://store.steampowered.com/search/?filter=topsellers')
soup = BeautifulSoup(response, 'html.parser')

# 게임 이름 가져오기
# result = soup.select("span.title")
# for i in result:
#     print(i.get_text())

# 게임 주소 가져오고 들어가서 카테고리 가져오기
result = soup.select("#search_resultsRows > a")
href = []
for i in result:
    temp = i.attrs['href']
    print(temp)
    href.append(temp)
    response = urlopen(temp)
    # result2 = soup.select("#game_highlights > div.rightcol > div > div.glance_ctn_responsive_right > div > div.glance_tags.popular_tags > a:nth-child(1)")
print(href)

