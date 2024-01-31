import os
import json
from datetime import datetime
import requests
from html import unescape
import html2text
import re
from typing import List, Optional, Dict
from bs4 import BeautifulSoup
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
#from httpx import URL, Proxy, Timeout, Response, ASGITransport, AsyncBaseTransport


#from component.Details_News import get_news_details_list

class FetchDetailsError(Exception):
    pass

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

# Function to call the Azure Chat API with a list of messages
def __call_chat_api(messages: list) -> AzureChatOpenAI:
    # Create an instance of the AzureChatOpenAI model
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    
    # Use a context manager to handle OpenAI API callbacks
    with get_openai_callback():
        # Call the AzureChatOpenAI model with the provided messages
        return model(messages)

    
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

def get_news_details_list():
    try:
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)

        # Extract news information
        news_list = extract_news_info(data)
        news_details_list = []

        for news in news_list:
            link = news.get('link', '')
            try:
                # Fetch details for each link
                news_details = get_news_details(link)
                details_news = news_details.get('content', '')

                if details_news:
                    # Append news details to the list
                    news_details_list.append(details_news)

            except FetchDetailsError as e:
                print(f"An error occurred while fetching details for link: {link}. {str(e)}")
                # traceback.print_exc()  # Print the traceback for the exception

        return news_details_list

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        # traceback.print_exc()  # Print the traceback for the exception
        return None



def remove_unnecessary_text(details_feed):
    # Remove HTML tags
    cleaned_details_feed = re.sub(r'<.*?>', '', details_feed)
    
    # Remove any other specific patterns or text you want to exclude
   # Remove lines starting with specific keywords
    cleaned_details_feed = re.sub(r'^\s*(?:unwanted1|unwanted2|unwanted3).*$', '', cleaned_details_feed, flags=re.MULTILINE)
     # Remove lines containing specific keywords
    keywords_to_remove = ['unwanted1', 'unwanted2', 'unwanted3', 'image', 'picture', 'photo']
    for keyword in keywords_to_remove:
        cleaned_details_feed = re.sub(fr'\b{keyword}\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)

    # Remove lines that seem like ads
    cleaned_details_feed = re.sub(r'\b(?:ad|advertisement|promo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    # Remove lines that seem like image captions
    cleaned_details_feed = re.sub(r'\b(?:image|picture|photo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    # Remove extra whitespace
    cleaned_details_feed = re.sub(r'\s+', ' ', cleaned_details_feed).strip()
    
    return cleaned_details_feed
def format_news_details(details_feed):
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(details_feed, 'html.parser')
    cleaned_details_feed = soup.get_text(separator=' ')

    # Remove extra whitespace
    cleaned_details_feed = ' '.join(cleaned_details_feed.split())

    return cleaned_details_feed

def create_article(formatted_details_feed, source_link):
    # Generate an article from the cleaned and formatted news details
    article = f"Article for News Details:\n\n{formatted_details_feed}\n\nRead more at the source link: {source_link}"
    return article

def analysis_and_recommendation():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]
    
    # Obtain the list of news details
    news_details_list = get_news_details_list()

    for details_feed in news_details_list:
        # Step 1: Remove unnecessary text
        cleaned_details_feed = remove_unnecessary_text(details_feed)

        # Step 2: Format news details
        formatted_details_feed = format_news_details(cleaned_details_feed)

        # Step 3: Generate article
        if isinstance(details_feed, dict):
         source_link = details_feed.get('link', '')
        else:
    # Handle the case when details_feed is not a dictionary
         source_link = ''  # or any other default value that makes sense in your context
        print("Warning: details_feed is not a dictionary.")

        article = create_article(formatted_details_feed, source_link)

        # Make the API call to generate a response for each news detail
        response = __call_chat_api(request_messages)

        # Convert content_from_api to string
        content_from_api = response.content if isinstance(response, AIMessage) else str(response)

        # Extend the request_messages with the content for further processing
        request_messages.extend([
            AIMessage(content=content_from_api),
            HumanMessage(content=f"Create Summary article for news details return a json format where key will be date and value will be Id,title,link,article:\n{article}")
        ])

        # Make another API call with updated messages to generate a summary
        response_summary = __call_chat_api(request_messages).content
        response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)
        print(response_summary_str)

analysis_and_recommendation()
