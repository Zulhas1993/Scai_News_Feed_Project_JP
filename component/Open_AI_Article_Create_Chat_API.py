import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import html2text
from typing import Dict, List
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

# Custom exception class for handling fetch details errors
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
    def __init__(self, feed_id, title, ex_link, details_news):
        self.feed_id = feed_id
        self.title = title
        self.ex_link = ex_link
        self.details_news = details_news



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

#************************** News Details ************************

def get_news_details(link):
    try:
        # Send an HTTP GET request to the provided link
        response = requests.get(link)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Convert HTML text to plain text using html2text library
        details_text = html2text.html2text(soup.get_text())

        # Check if the details text is not empty or consists only of whitespace
        if details_text and not details_text.isspace():
            # Return the details content as a dictionary
            return {'content': details_text.strip()}
        else:
            # Return None if details text is empty or consists only of whitespace
            return None

    except requests.RequestException as e:
        # Raise a custom exception if there is an error fetching details
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")


#***************************News Details List **********************************

def get_news_details_list() -> List[Dict[str, str]]:
    try:
        # Specify the file path containing the news data in JSON format
        file_path = 'object_list1.json'

        # Read the JSON data from the specified file
        data = read_json(file_path)

        # Initialize an empty list to store news details
        news_details_list = []

        # Iterate through each category and its feed entries in the JSON data
        for category, feed_entries in data.items():
            for index, news in feed_entries.items():
                # Check if the news entry is a valid dictionary
                if not isinstance(news, dict):
                    try:
                        # Attempt to convert the news entry to a dictionary
                        news = json.loads(news)

                        # Raise an error if the conversion is not successful
                        if not isinstance(news, dict):
                            raise ValueError("Converted news is not a dictionary.")

                    except (json.JSONDecodeError, ValueError) as error:
                        # Handle errors during the conversion process
                        print(f"Warning: Unable to convert news at index {index} in category {category} to a dictionary. {error}")
                        continue

                # Extract the 'link' attribute from the news entry
                link = news.get('link', '')

                try:
                    # Fetch details for the news using the 'get_news_details' function
                    news_details = get_news_details(link)

                    # Check if the fetched news details are in the expected format
                    if news_details and isinstance(news_details, dict) and 'content' in news_details:
                        details_news = news_details.get('content', '')
                    else:
                        # Handle cases where the news details are not in the expected format
                        print(f"Warning: Invalid format for news details at index {index} in category {category}. Skipping.")
                        continue

                    # Check if 'details_news' is a valid string
                    if not isinstance(details_news, str):
                        print(f"Warning: 'details_news' at index {index} is not a valid string. Skipping.")
                        continue

                    # Append a dictionary with Title, Link, and details_news to the news_details_list
                    news_details_list.append({
                        'Id': len(news_details_list) + 1,  # Auto-incrementing Id
                        'CurrentDate': "",  # Add the current date logic here
                        'title': news.get('title', ''),
                        'link': link,
                        'details_news': details_news
                    })

                except Exception as e:
                    # Handle errors that occur during the fetching of news details
                    print(f"An error occurred while fetching details for news at index {index} in category {category}. {str(e)}")

        # Return the list of news details
        return news_details_list

    except Exception as e:
        # Handle general errors that occur during the retrieval of news details
        print(f"An error occurred during news details retrieval: {e}")

        # Return an empty list in case of an error
        return []


#****start**************** Article List ********************

def get_articles_list():
    # Initialize a list to store the generated articles
    articles_list = []

    # Starting Id for articles
    current_feed_id = 100
    current_article_id = 1

    # Get news details list using the 'get_news_details_list' function
    news_details_list = get_news_details_list()

    # Initialize request messages for the Chat AI
    request_messages = [SystemMessage(content="Please answer in English")]

    # Iterate through each news details entry
    for details_feed in news_details_list:
        try:
            # Check if the entry is a dictionary
            if isinstance(details_feed, dict):
                # Increment Id for each article
                current_feed_id += 1
                current_article_id += 1

                # Create a NewsFeed object from details_feed
                news_entry = NewsFeed(
                    feed_id=current_feed_id,
                    title=details_feed.get('title', ''),
                    ex_link=details_feed.get('link', ''),
                    details_news=details_feed.get('details_news', '')
                )

                # Convert the NewsFeed object to a dictionary
                news_dict = news_entry.__dict__

                # Generate article using Chat AI
                response = __call_chat_api(request_messages)
                content_from_api = response.content if isinstance(response, AIMessage) else str(response)
                created_article = str(content_from_api)

                # Extend request_messages to include a message about creating an article
                request_messages.extend([
                    AIMessage(content=created_article),
                    HumanMessage(f"Create Summary article for each details news, if any link or details news have a problem creating an article, skip the details news and continue for the next details news. Create articles one by one, and all articles will be within 150 words. The response format is Title:, Link:, Article: \n{json.dumps(news_dict, ensure_ascii=False)}")
                ])

                # Generate summary using Chat AI
                response_summary = __call_chat_api(request_messages)
                response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)

                # Extract the 'Article' part from response_summary_str
                article_start_index = response_summary_str.find('Article:')
                if article_start_index != -1:
                    article_text = response_summary_str[article_start_index + len('Article:'):].strip()
                else:
                    article_text = ""

                # Add Link, Title, Article, and Article ID to the list
                current_date = datetime.now().strftime("%Y-%m-%d")
                articles_list.append({
                    'feed_id': news_entry.feed_id,
                    'article_id': current_article_id,
                    'Link': news_dict.get('ex_link', ''),
                    'title': news_dict.get('title', ''),
                    'article': article_text,
                    'date': current_date
                })

            else:
                print("Warning: details_feed is not a dictionary.")

        except Exception as e:
            # Handle errors that occur during the generation of articles
            print(f"An error occurred: {e}")
            continue

    # Return the list of generated articles
    return articles_list




## *******************************It return a json for NewsFeed *******************************************


# def analysis_and_recommendation():
#     request_messages = [SystemMessage(content="Please answer in English")]

#     articles_dict = {}  # To store the generated articles
#     current_id = 1000  # Starting Id

#     news_details_list = get_news_details_list()

#     for details_feed in news_details_list:
#         try:
#             if isinstance(details_feed, dict):
#                 current_id += 1  # Increment Id for each article

#                 news_entry = NewsFeed(
#                     id=current_id,  
#                     title=details_feed.get('title', ''),
#                     tags="",  
#                     ex_link=details_feed.get('link', ''),
#                     description="",  
#                     details_news=details_feed.get('details_news', ''),
#                     keywords="",  
#                     article="",  
#                     date=""  
#                 )

#                 news_dict = news_entry.__dict__

#                 # Generate article using Chat AI
#                 response = __call_chat_api(request_messages)
#                 content_from_api = response.content if isinstance(response, AIMessage) else str(response)
#                 created_article = str(content_from_api)

#                 # Extend request_messages to include the message about creating an article
#                 request_messages.extend([
#                     AIMessage(content=created_article),
#                     HumanMessage(content=f"Create Summary article for each details news , if any link or details news have a problem to creating article you skip the details news and continue for next details news and Create article one by one and all article will be within 150 words and response format is Title: , Link: ,Article  :\n{json.dumps(news_dict, ensure_ascii=False)}")
#                 ])

#                 # Generate summary using Chat AI
#                 response_summary = __call_chat_api(request_messages)
#                 response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)

#                 # Extract the 'Article' part from response_summary_str
#                 article_start_index = response_summary_str.find('Article:')
#                 if article_start_index != -1:
#                     article_text = response_summary_str[article_start_index + len('Article:'):].strip()
#                 else:
#                     article_text = ""
                
#                 # Convert news_dict to a JSON-formatted dictionary with the extracted article
#                 current_date = datetime.now().strftime("%Y-%m-%d")
#                 article_dict = {
#                     'CurrentDate': current_date,  
#                     'title': news_dict.get('title', ''),
#                     'link': news_dict.get('ex_link', ''),
#                     'detailsNews': news_dict.get('details_news', ''),  # Corrected key
#                     'article': article_text  # Use extracted article_text as the article content
#                 }

#                 # Add the article to the dictionary with the current_id as the key
#                 articles_dict[current_id] = article_dict


#             else:
#                 print("Warning: details_feed is not a dictionary.")

#         except Exception as e:
#             print(f"An error occurred: {e}")
#             continue

#     # Print the response as JSON format
#     print(json.dumps(articles_dict, ensure_ascii=False, indent=2))


# Call the analysis_and_recommendation function
#analysis_and_recommendation()









