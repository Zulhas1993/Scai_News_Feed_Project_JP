import json
import requests
from bs4 import BeautifulSoup

def read_json(file_path):
    with open(file_path,'r',encoding='utf-16') as file
    data=json.load(file)
    return data


def extrct_news_info(data):
    news_list=[]
    unique_link=set()
    for key, value in data.items():
        for entry in value.values():
            entry_data=json.load(entry)
            title =entry_data.get('title', '')
            link=entry_data.get('link','')
            description=entry_data.get('description','')
            tags=entry_data.get('tags',[])
            if link not in unique_link and description:
                news_list.append({'title':title,'link':link,'description': description,'tags':tags})
                unique_link.add(link)
    return news_list

          
        

