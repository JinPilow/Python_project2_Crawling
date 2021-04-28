from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('https://store.steampowered.com/search/?filter=topsellers')
soup = BeautifulSoup(response, 'html.parser')
result = soup.select("#search_resultsRows > span.title")
print(result)
# for title in result:
#     print(title.get())