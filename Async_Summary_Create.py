import os
import json
import requests
import re
import asyncio
from bs4 import BeautifulSoup
from html import unescape
import html2text
from typing import List, Optional, Dict
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

class FetchDetailsError(Exception):
    pass

async def __call_chat_api(messages: list) -> AzureChatOpenAI:
    # Create an instance of the AzureChatOpenAI model
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    
    # Use a context manager to handle OpenAI API callbacks
    with get_openai_callback():
        # Call the AzureChatOpenAI model with the provided messages
        return model(messages)  # use await here


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
        # Open the JSON file in read mode using utf-16 encoding
        with open(file_path, 'r', encoding='utf-16') as file:
            
            # Load the JSON data from the file
            data = json.load(file)
            
        # Return the loaded data
        return data
    
    # Handle exceptions that may occur during file reading or JSON decoding
    except Exception as e:
        
        # Print an error message indicating the issue
        print(f"Error reading JSON file: {e}")
        
        # Return None to indicate an unsuccessful operation
        return None

# Function to extract relevant information from a nested data structure
def extract_news_info(data):
    # Initialize an empty list to store extracted news information
    news_list = []
    
    # Use a set to keep track of unique links to avoid duplicates
    unique_links = set()  

    # Iterate through the nested data structure
    for key, value in data.items():
        for entry in value.values():
            # Parse the JSON data within each entry
            entry_data = json.loads(entry)
            
            # Extract relevant information from the parsed data
            title = entry_data.get('title', '')
            link = entry_data.get('link', '')
            description = entry_data.get('description', '')
            subjectList = entry_data.get('subjectList', [])

            # Check if the link is not a duplicate and has a description
            if link not in unique_links and description:
                # Append a dictionary containing extracted information to the news_list
                news_list.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'subjectList': subjectList
                })
                # Add the link to the set to track uniqueness
                unique_links.add(link)
               
    # Return the list of extracted news information
    return news_list

def get_news_details(link):
    try:
        # You can customize this function to fetch news details from the provided link
        response = requests.get(link)
        # print(f"Response Status Code: {response.status_code}")
        # response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Use html2text to convert HTML content to plain text
        details_text = html2text.html2text(soup.get_text())

        # Check if the details_text is not empty or contains only whitespace
        if details_text and not details_text.isspace():
            # Return the news details
            return {'content': details_text.strip()}
        else:
            # Return None if there are no details
            return None
    except requests.RequestException as e:
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")
def get_news_details_list(batch_size=10):
    try:
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)

        # Extract news information
        news_list = extract_news_info(data)
        news_details_list = []

        for i in range(0, len(news_list), batch_size):
            batch = news_list[i:i + batch_size]

            for news in batch:
                link = news.get('link', '')
                title = news.get('title', '')
                description = news.get('description', '')
                subjectList = news.get('subjectList', [])
                tags = ""

                try:
                    # Fetch details for each link
                    news_details = get_news_details(link)
                    details_news = news_details.get('content', '')

                    if details_news:
                        # Append news details to the list
                        news_details_list.append({
                            'title': title,
                            'link': link,
                            'tags': tags,
                            'description': description,
                            'subjectList': subjectList,
                        })

                except FetchDetailsError as e:
                    print(f"An error occurred while fetching details for link: {link}. {str(e)}")
                    # traceback.print_exc()  # Print the traceback for the exception
                    continue

        return news_details_list

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        # traceback.print_exc()  # Print the traceback for the exception
        return None

def create_article(formatted_details_feed, source_link):
    # Generate an article from the cleaned and formatted news details
    article = f"Article for News Details:\n\n{formatted_details_feed}\n\nRead more at the source link: {source_link}"
    return article


async def analyze_news_details(news_details, request_messages):
    if isinstance(news_details, dict):
        source_link = news_details.get('link', '')
    else:
        source_link = ''

    news_entry = NewsFeed(
        id="",
        title=news_details.get('title', ''),
        tags="",
        ex_link=news_details.get('link', ''),
        description=news_details.get('description', ''),
        details_news=news_details,
        keywords="",
        article=create_article(news_details, source_link),
        date=""
    )

    news_dict = news_entry.__dict__

    response = await __call_chat_api(request_messages)
    
    if response is not None:
        content_from_api = response.content if isinstance(response, AIMessage) else str(response)
        content_str = str(content_from_api)

        request_messages.extend([
            AIMessage(content=content_str),
            HumanMessage(content=f"Create Summary article for each details news  :\n{news_dict}")
        ])

        # Make another API call with updated messages to generate a summary
        response_summary = await __call_chat_api(request_messages)
        response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)
        print(response_summary_str)



async def analysis_and_recommendation():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]

    # Obtain the list of news details
    news_details_list = get_news_details_list()

    tasks = []
    for news_details in news_details_list:
        tasks.append(analyze_news_details(news_details, request_messages))
        asyncio.sleep(1)  # pause for 1 second before the next iteration

    # Gather the tasks after the loop
        asyncio.gather(*tasks)


# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(analysis_and_recommendation())
