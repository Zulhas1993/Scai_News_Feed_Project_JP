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
    allLinksByCategoryDict = {}
    #print("scrap feeds")

    try:
        for category in categories:
            content = urlopen(url + category).read()
            linksWithTitle = getLinksWithTitle(content)
            allLinksByCategoryDict[category] = linksWithTitle

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    #print(categories)

    return allLinksByCategoryDict


def get_all_links(allLinksByCategoryDict):
    all_links_list = []

    try:
        for key, value in allLinksByCategoryDict.items():
            #print(f"Processing key: {key}")
            if isinstance(value, dict):
                for obj_id, obj in value.items():
                    if isinstance(obj, str):
                        try:
                            obj_dict = json.loads(obj)
                            if isinstance(obj_dict, dict):
                                all_links_list.append(obj_dict)
                        except json.JSONDecodeError:
                            print(f"Unable to decode JSON for key {key}, obj_id {obj_id}: {obj}")
                    else:
                        print(f"Value for key {key} and obj_id {obj_id} is not a string")

            else:
                print(f"Value for key {key} is not a dictionary")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    #print(f"all links: {all_links_list}")
    return all_links_list

# allLinksByCategoryDict = fillDictionaryWithData()
# all_links_list = get_all_links(allLinksByCategoryDict)

# Now 'all_links_list' contains a list of dictionaries
# print(all_links_list)