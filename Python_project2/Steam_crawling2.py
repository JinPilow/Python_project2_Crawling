from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://store.steampowered.com/search/?sort_by=_ASC&os=win&filter=globaltopsellers')
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
    href.append(temp)
    response = urlopen(temp)
    soup = BeautifulSoup(response, 'html.parser')
    result2 = soup.select("a.app_tag")
    for j in result2:
        print(j.get_text())
    print("--------------------------------------------------------------------------")
# print(href)

