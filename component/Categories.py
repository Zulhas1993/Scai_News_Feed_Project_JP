from urllib.request import urlopen
from bs4 import BeautifulSoup


def getCategories(baseUrl):
    urlContent = str(urlopen(baseUrl).read())
    allCategories = [];
    soup = BeautifulSoup(urlContent, 'html.parser')
    ulElement = soup.find_all('ul',class_='js-navi-category')
    liFromUlElement = ulElement[0].find_all('li',class_='js-navi-category-item')
    for item in liFromUlElement:
        allAnchorElement = item.find_all("a", class_="navi-link-text")
        allCategories.append(allAnchorElement[0].get('href')+'.rss')

    return allCategories