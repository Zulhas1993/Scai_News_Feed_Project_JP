from urllib.request import urlopen
from bs4 import BeautifulSoup
from Categories import getCategories
import json

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
    return linkWithTitle

def fillDictionaryWithData():
    for category in categories:
        content = urlopen(url + category).read()
        linksWithTitle = getLinksWithTitle(content)
        allLinksByCategoryDict[category] = linksWithTitle

def get_all_links():
    all_links_list = []

    try:
        # Print debugging statement to check if allLinksByCategoryDict is not empty
        print("allLinksByCategoryDict:", allLinksByCategoryDict)

        # Iterate over keys of allLinksByCategoryDict
        for category in allLinksByCategoryDict.keys():
            # Print debugging statement to check if linksWithTitle is not empty
            print(f"Category: {category}, linksWithTitle: {allLinksByCategoryDict[category]}")

            # Iterate over values of a specific category
            for link_id, link_data in allLinksByCategoryDict[category].items():
                if isinstance(link_data, dict):
                    link_info = {
                        'title': link_data.get('title', ''),
                        'link': link_data.get('link', ''),
                        'description': link_data.get('description', ''),
                        'tags': link_data.get('tags', {})
                    }
                    all_links_list.append(link_info)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Convert the list to JSON format
    all_links_json = json.dumps(all_links_list, ensure_ascii=False, indent=2)
    return all_links_json

fillDictionaryWithData()
response = get_all_links()
print(response)
