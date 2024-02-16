from component.Scrapping_Feeds import get_all_links
from component.Details_News import extract_news_info, read_json
from component.Open_AI_Article_Create_Chat_API import get_news_details_list,get_articles_list
from component.Article_list import get_articles_list
import json

file_path = 'object_list_empty.json'

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data


scrapping_data = get_all_links()
extract_news_info_from_scrapping_data = extract_news_info(read_json(file_path))
news_details_list=get_news_details_list()
print (news_details_list)

#artcle_list=get_articles_list()

#print(extract_news_info_from_scrapping_data)
