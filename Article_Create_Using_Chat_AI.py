import os
import json
import requests
import re
import time
from bs4 import BeautifulSoup
import html2text
from typing import Dict, List
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

class FetchDetailsError(Exception):
    pass

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    
    with get_openai_callback():
        return model(messages)

class NewsFeed:
    def __init__(self, id, title, tags, ex_link, description, details_news, keywords, article, date):
        self.id = id
        self.title = title
        self.tags = tags
        self.ex_link = ex_link
        self.description = description
        self.details_news = details_news
        self.keywords = keywords
        self.article = article
        self.date = date

# Function to read JSON data from a file
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            data = json.load(file)
            print(f"Data loaded from {file_path}: {data}")
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def get_news_details(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        details_text = html2text.html2text(soup.get_text())

        if details_text and not details_text.isspace():
            return {'content': details_text.strip()}
        else:
            return None
    except requests.RequestException as e:
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")

def get_news_details_list() -> List[Dict[str, str]]:
    try:
        file_path = 'object_list.json'
        data = read_json(file_path)
        news_details_list = []

        for category, feed_entries in data.items():
            for index, news in feed_entries.items():
                if not isinstance(news, dict):
                    try:
                        news = json.loads(news)
                        if not isinstance(news, dict):
                            raise ValueError("Converted news is not a dictionary.")
                    except (json.JSONDecodeError, ValueError) as error:
                        print(f"Warning: Unable to convert news at index {index} in category {category} to a dictionary. {error}")
                        continue

                link = news.get('link', '')

                try:
                    news_details = get_news_details(link)

                    if news_details and isinstance(news_details, dict) and 'content' in news_details:
                        details_news = news_details.get('content', '')
                    else:
                        print(f"Warning: Invalid format for news details at index {index} in category {category}. Skipping.")
                        continue

                    if not isinstance(details_news, str):
                        print(f"Warning: 'details_news' at index {index} is not a valid string. Skipping.")
                        continue

                    # Append a dictionary with Title, Link, and details_news to the news_details_list
                    news_details_list.append({
                        'Title': news.get('title', ''),
                        'Link': link,
                        'details_news': details_news
                    })

                except Exception as e:
                    print(f"An error occurred while fetching details for news at index {index} in category {category}. {str(e)}")

        return news_details_list

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        return []

def analysis_and_recommendation():
    request_messages = [SystemMessage(content="Please answer in English")]

    news_details_list = get_news_details_list()

    for details_feed in news_details_list:
        try:
            if isinstance(details_feed, dict):
                news_entry = NewsFeed(
                    id="",  
                    title=details_feed.get('Title', ''),
                    tags="",  
                    ex_link=details_feed.get('Link', ''),
                    description="",  
                    details_news=details_feed.get('details_news', ''),
                    keywords="",  
                    article="",  
                    date=""  
                )

                news_dict = news_entry.__dict__

                response = __call_chat_api(request_messages)
                content_from_api = response.content if isinstance(response, AIMessage) else str(response)
                content_str = str(content_from_api)

                request_messages.extend([
                    AIMessage(content=f"{content_str}"),
                    HumanMessage(content=f"When generating this error: Azure has not provided the response due to a content filter being triggered. Skipping this and continuing to the next news entry")
                ])

                request_messages.extend([
                    AIMessage(content=content_str),
                    HumanMessage(content=f"Create Summary article for each details news , if any link or details news have a problem to creating article you skip the  details news and continue for next details news and Create article one by one and all article will be within 150 words and response format is Title: , Link: ,Article  :\n{news_dict}")
                ])

                response_summary = __call_chat_api(request_messages)
                response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)
                print(response_summary_str)

            else:
                print("Warning: details_feed is not a dictionary.")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        finally:
            request_messages = [SystemMessage(content="Please answer in English")]
            time.sleep(1)

# Call the analysis_and_recommendation function
analysis_and_recommendation()
