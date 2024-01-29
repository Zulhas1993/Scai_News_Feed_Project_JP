import json
import requests
from datetime import datetime
import html2text
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
import re
from typing import List, Optional, Dict
class FetchDetailsError(Exception):
    pass


def authenticate_client():
    try:
        endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
        key = "09b7c88cfff44bac95c83a2256f31907"
        return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            data = json.load(file)
            print(f"Data loaded from {file_path}: {data}")
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

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


def extract_news_info(data):
    # Initialize an empty list to store extracted news information
    news_list = []

    # Create a set to track unique links and avoid duplicates
    unique_links = set()

    # Loop through categories and their entries in the provided data
    for key, value in data.items():
        # Loop through individual news entries in the current category
        for entry in value.values():
            # Parse the JSON data for the current news entry
            entry_data = json.loads(entry)

            # Extract relevant information from the news entry
            title = entry_data.get('title', '')
            link = entry_data.get('link', '')
            description = entry_data.get('description', '')
            subjectList = entry_data.get('subjectList', [])

            # Check if the link is not a duplicate and the description is present
            if link not in unique_links and description:
                # Add the extracted information to the news_list
                news_list.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'subjectList': subjectList
                })

                # Mark the link as processed to avoid duplicates
                unique_links.add(link)

    # Return the list of extracted news information
    return news_list


def get_news_details(link):
    try:
        # Make a GET request to the provided link
        response = requests.get(link)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Use html2text to convert HTML to plain text
        details_text = html2text.html2text(soup.get_text())

        # Check if the extracted text is not empty or just whitespace
        if details_text and not details_text.isspace():
            # Return the details in a dictionary with 'content' key
            return {'content': details_text.strip()}
        else:
            # If the extracted text is empty or just whitespace, return None
            return None

    except requests.RequestException as e:
        # If an exception occurs during the request, raise a custom exception
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")

def get_news_details_list() -> Dict[str, str]:
    try:
        # File path of the JSON file containing news data
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)
        
        # Dictionary to store news details
        news_details_dict = {}

        # Iterate through categories and news entries
        for category, feed_entries in data.items():
            for index, news in feed_entries.items():
                # Convert news to a dictionary if it's not already
                if not isinstance(news, dict):
                    try:
                        news = json.loads(news)
                        if not isinstance(news, dict):
                            raise ValueError("Converted news is not a dictionary.")
                    except json.JSONDecodeError as json_error:
                        print(f"Warning: Unable to convert news at index {index} in category {category} to a dictionary. JSON decoding error: {json_error}")
                        continue
                    except ValueError as value_error:
                        print(f"Warning: Unable to convert news at index {index} in category {category} to a dictionary. {value_error}")
                        continue

                # Extract link from news entry
                link = news.get('link', '')
                try:
                    # Fetch details for each news
                    news_details = get_news_details(link)
                    details_news = news_details.get('content', '')

                    if details_news:
                        # Check if details_news is a valid JSON string
                        try:
                            json.loads(details_news)
                            news_details_dict[index] = details_news
                        except json.JSONDecodeError as json_error:
                            print(f"Warning: 'details_news' at index {index} is not a valid JSON string. Skipping. JSON decoding error: {json_error}")
                            # Uncomment the following line to print the content of 'details_news'
                            # print(f"Details News Content: {details_news}")

                except FetchDetailsError as e:
                    print(f"An error occurred while fetching details for news at index {index} in category {category}. {str(e)}")

        return news_details_dict

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        return {}





def remove_unnecessary_text(details_feed):
    # Remove HTML tags
    cleaned_details_feed = re.sub(r'<.*?>', '', details_feed)
    
    # Remove lines starting with specified patterns
    cleaned_details_feed = re.sub(r'^\s*(?:unwanted1|unwanted2|unwanted3).*$', '', cleaned_details_feed, flags=re.MULTILINE)
    
    # Keywords to remove
    keywords_to_remove = ['unwanted1', 'unwanted2', 'unwanted3', 'image', 'picture', 'photo']
    
    # Remove lines containing specified keywords
    for keyword in keywords_to_remove:
        cleaned_details_feed = re.sub(fr'\b{keyword}\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove lines containing specific terms related to ads
    cleaned_details_feed = re.sub(r'\b(?:ad|advertisement|promo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove lines containing terms related to images
    cleaned_details_feed = re.sub(r'\b(?:image|picture|photo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    
    # Replace consecutive whitespaces with a single space and strip leading/trailing spaces
    cleaned_details_feed = re.sub(r'\s+', ' ', cleaned_details_feed).strip()
    
    return cleaned_details_feed


def format_news_details(details_feed):
    # Create a BeautifulSoup object to parse HTML content
    soup = BeautifulSoup(details_feed, 'html.parser')
    
    # Get the text content, separating different parts with a space
    cleaned_details_feed = soup.get_text(separator=' ')
    
    # Join consecutive whitespaces into a single space
    cleaned_details_feed = ' '.join(cleaned_details_feed.split())
    
    return cleaned_details_feed


def generate_abstractive_summary(text_analytics_client, document):
    # Start the abstractive summarization process
    poller = text_analytics_client.begin_abstract_summary(document)
    
    # Get the results of the summarization process
    abstract_summary_results = poller.result()
    
    # Iterate through the results
    for result in abstract_summary_results:
        # Check if the result is an abstractive summarization
        if result.kind == "AbstractiveSummarization":
            print("Summaries abstracted:")
            # Print each generated summary
            [print(f"{summary.text}\n") for summary in result.summaries]
        # Check if there is an error
        elif result.is_error is True:
            print("An error occurred with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))


def make_details_news_valid(details_news):
    # Check if details_news is a dictionary
    if not isinstance(details_news, dict):
        # If not, create an empty dictionary
        details_news = {}

    # Add necessary fields or perform other modifications to make it valid
    if 'content' not in details_news:
        # If 'content' is missing, add a default value
        details_news['content'] = 'No content available.'

    return details_news

def create_article(formatted_details_feed, source_link):
    # Generate an article from the cleaned and formatted news details
    article = f"Article for News Details:\n\n{formatted_details_feed}\n\nRead more at the source link: {source_link}"
    return article



def generate_abstractive_summaries(text_analytics_client):
    try:
        # Initialize a dictionary to store all generated summaries
        all_summaries_dict = {}
        
        # Retrieve news details as a dictionary
        news_details_list = get_news_details_list()

        # Check if the retrieved news_details_list is a dictionary
        if not isinstance(news_details_list, dict):
            try:
                # Attempt to convert news_details_list to a dictionary
                news_details_list = json.loads(news_details_list)
                
                # Check if the conversion was successful
                if not isinstance(news_details_list, dict):
                    raise ValueError("Converted news_details_list is not a dictionary.")
            except json.JSONDecodeError as json_error:
                print(f"Error: Unable to convert news_details_list to a dictionary. JSON decoding error: {json_error}")
                return None
            except ValueError as value_error:
                print(f"Error: Unable to convert news_details_list to a dictionary. {value_error}")
                return None

        # Iterate through each news entry in the news_details_list
        for news_date, news_details in news_details_list.items():
            try:
                # Check if news_details is a dictionary
                if not isinstance(news_details, dict):
                    news_details = json.loads(news_details)

                # Extract 'details_news' from the news_details dictionary
                details_news = news_details.get('details_news', {})

                # Check if 'details_news' is a dictionary
                if not isinstance(details_news, dict):
                    print(f"Warning: 'details_news' is not a dictionary. Content: {details_news}")
                    continue

                # Generate abstractive summaries using the Text Analytics client
                summaries = generate_abstractive_summary(text_analytics_client, details_news)

                # Check if summaries were successfully generated
                if summaries is not None:
                    # Store the generated summaries in the all_summaries_dict
                    all_summaries_dict[news_date] = {
                        'id': news_details.get('id', ''),
                        'title': news_details.get('title', ''),
                        'summaries': summaries
                    }
            except json.JSONDecodeError as json_error:
                print(f"Error: Unable to convert news_details to a dictionary. JSON decoding error: {json_error}")
            except ValueError as value_error:
                print(f"Error: Unable to convert news_details to a dictionary. {value_error}")
            except Exception as e:
                print(f"An error occurred during abstractive summarization: {e}")

        # Write the generated summaries to a JSON file
        output_file_path = 'summaries_output.json'
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_summaries_dict, json_file, ensure_ascii=False, indent=2)

        print(f"Summaries have been written to {output_file_path}")
        return all_summaries_dict

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return None

# Assume you have an implementation for authenticating the text_analytics_client

# Authenticate the Text Analytics client
text_analytics_client = authenticate_client()

# Check if authentication was successful
if text_analytics_client is not None:
    # Generate abstractive summaries using the authenticated Text Analytics client
    generate_abstractive_summaries(text_analytics_client)
else:
    print("Authentication failed. Check your credentials.")







