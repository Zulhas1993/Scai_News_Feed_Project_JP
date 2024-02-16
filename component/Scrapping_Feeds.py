from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


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

url = 'https://b.hatena.ne.jp'
allLinksByCategoryDict = {}
categories = getCategories(baseUrl=url)

class LinkWithTitle:
    def __init__(self, title, link, description, tagDict):
        self.title = title
        self.link = link
        self.description = description
        self.tags = tagDict

    def toJson(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False)




def getLinksWithTitle(content):
    linkWithTitle = {}

    soup = BeautifulSoup(content, 'xml')
    allFetchedElements = soup.find_all('item')
    countItem = 1
    for element in allFetchedElements:
        _tagDict = {}
        _title = element.find_all('title')[0].contents[0]
        _link = element.find_all('link')[0].contents[0]

        # Check if 'description' elements exist and are not empty
        description_elements = element.find_all('description')
        _description = description_elements[0].contents[0].strip() if description_elements and description_elements[0].contents else ''

        _subjectWithTags = element.find_all('dc:subject')
        countTag = 1
        for subjectElement in _subjectWithTags:
            _tagDict[countTag] = subjectElement.contents[0]
            countTag = countTag + 1

        obj = LinkWithTitle(title=_title, link=_link, description=_description, tagDict=_tagDict)
        linkWithTitle[countItem] = obj.toJson()
        countItem = countItem + 1
        print(linkWithTitle)
    return linkWithTitle




def fillDictionaryWithData():
    for category in categories:
        content = urlopen(url + category).read()
        linksWithTitle = getLinksWithTitle(content)
        allLinksByCategoryDict[category] = linksWithTitle



def get_all_links():
    all_links_list = []

    try:
        # Assuming you have already defined and filled the 'allLinksByCategoryDict' dictionary
        for key, value in allLinksByCategoryDict.items():
            for obj_id, obj in value.items():
                if isinstance(obj, dict):  # Check if obj is a dictionary
                    link_data = {
                        'title': obj.get('title', ''),
                        'link': obj.get('link', ''),
                        'description': obj.get('description', ''),
                        'tags': obj.get('tags', {})
                    }
                    all_links_list.append(link_data)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Convert the list to JSON format
    all_links_json = json.dumps(all_links_list, ensure_ascii=False, indent=2)
    #print(all_links_json)
    return all_links_json




fillDictionaryWithData()
# all_links_list = get_all_links()

