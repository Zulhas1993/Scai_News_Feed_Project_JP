import json
import requests
import re
from bs4 import BeautifulSoup
from typing import Dict
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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

# Function to read JSON data from a file
def read_json(file_path):
    try:
        # Open the JSON file in read mode using utf-16 encoding
        with open(file_path, 'r', encoding='utf-16') as file:
            
            # Load the JSON data from the file
            data = json.load(file)
            
            # Print a message indicating successful loading of data
            print(f"Data loaded from {file_path}: {data}")
            
        # Return the loaded data
        return data
    
    # Handle exceptions that may occur during file reading or JSON decoding
    except Exception as e:
        
        # Print an error message indicating the issue
        print(f"Error reading JSON file: {e}")
        
        # Return None to indicate an unsuccessful operation
        return None

# Function to retrieve details from a news article given its link
def get_news_details(link):
    try:
        # Send an HTTP GET request to the provided link
        response = requests.get(link)
        
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the HTML and remove extra whitespaces
        details_text = soup.get_text(separator=' ')
        
        # Return the extracted content as a dictionary
        return {'content': details_text.strip()}

    # Handle exceptions related to the HTTP request
    except requests.RequestException as e:
        return {'error': f"Error fetching details for link: {link}. {str(e)}"}
    
    # Handle unexpected exceptions
    except Exception as e:
        return {'error': f"Unexpected error: {str(e)}"}

def get_news_details_list() -> Dict:
    try:
        file_path = 'object_list.json'
        data = read_json(file_path)
        news_details_list = []

        for category, feed_entries in data.items():
            for index, news in feed_entries.items():
                # Convert news to a dictionary if it's not already
                if not isinstance(news, dict):
                    try:
                        news = json.loads(news)
                        if not isinstance(news, dict):
                            raise ValueError("Converted news is not a dictionary.")
                    except (json.JSONDecodeError, ValueError) as error:
                        print(f"Warning: Unable to convert news at index {index} in category {category} to a dictionary. {error}")
                        continue

                # Extract link from news entry
                link = news.get('link', '')

                try:
                    # Fetch details for each news
                    news_details = get_news_details(link)

                    # Check if the result is not None and is a dictionary with a 'content' key
                    if news_details and isinstance(news_details, dict) and 'content' in news_details:
                        # Extract 'details_news' if available, otherwise set it to an empty dictionary
                        details_news = news_details.get('content', '')
                    else:
                        # Print a warning and skip if the result is not in the expected format
                        print(f"Warning: Invalid format for news details at index {index} in category {category}. Skipping.")
                        continue

                    # Ensure details_news is a string
                    if not isinstance(details_news, str):
                        print(f"Warning: 'details_news' at index {index} is not a valid string. Skipping.")
                        continue

                    news_details_list.append(details_news)

                except Exception as e:
                    # Print an error message if an exception occurs during fetching details
                    print(f"An error occurred while fetching details for news at index {index} in category {category}. {str(e)}")

        return news_details_list

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        return []

def remove_unnecessary_text(details_feed):
    # Replace this function with your specific implementation
    # Remove unwanted HTML tags, patterns, keywords, etc.
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
    cleaned_details_feed = " ".join(cleaned_details_feed.split())
    
    # Remove any trailing commas if present
    cleaned_details_feed = cleaned_details_feed.rstrip(',')
    
    # Return the cleaned details within double quotes
    return f'"{cleaned_details_feed}"'

# Function to generate abstractive summaries using Azure Text Analytics service
def generate_abstractive_summary(text_analytics_client, documents, max_summary_words=150):
    try:
        # Begin the process of generating abstract summaries using the provided documents
        poller = text_analytics_client.begin_abstract_summary(documents)

        # Wait for the operation to complete and get the results
        abstract_summary_results = poller.result()

        # Initialize an empty list to store the generated summaries
        summaries = []

        # Iterate through the results
        for result in abstract_summary_results:
            # Check if the result represents abstractive summarization
            if result.kind == "AbstractiveSummarization":
                # Iterate through each summary in the result
                for summary in result.summaries:
                    # Split the summary into words
                    words = summary.text.split()

                    # Check if the summary is within the desired word count
                    if len(words) <= max_summary_words:
                        # Append the summary to the list
                        summaries.append(summary.text)
                    else:
                        # If the summary is too long, truncate it to the desired length
                        summaries.append(' '.join(words[:max_summary_words]))

        # Return the generated summaries
        return summaries

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return []

# Rest of your code...




def generate_abstractive_summaries(text_analytics_client):
    try:
        all_summaries = {}
        news_details_list = get_news_details_list()

        for index, news_details in enumerate(news_details_list, start=1):
            try:
                # Ensure 'news_details' is a string
                if not isinstance(news_details, str):
                    print(f"Warning: 'news_details' is not a valid string. Skipping.")
                    continue

                # Remove unnecessary text
                cleaned_details = remove_unnecessary_text(news_details)

                # Format news details
                formatted_details = format_news_details(cleaned_details)

                # Generate abstractive summary
                summaries = generate_abstractive_summary(text_analytics_client, [formatted_details])

                if summaries:
                    # Generate article_key
                    article_key = f"article_{index}"

                    # Add the summaries to the dictionary
                    all_summaries[article_key] = summaries

            except Exception as e:
                # Print an error message if an exception occurs during summarization
                print(f"An error occurred during abstractive summarization: {e}")

        # Print or save the summaries as needed
        print("Summaries:")
        for article_key, summaries in all_summaries.items():
            print(f"{article_key}:")
            for summary in summaries:
                print(f"  {summary}")

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")

# Rest of your code...



# Assume you have an implementation for authenticating the text_analytics_client

# Authenticate the Text Analytics client
text_analytics_client = authenticate_client()

# Check if authentication was successful
if text_analytics_client is not None:
    # Generate abstractive summaries using the authenticated Text Analytics client
    generate_abstractive_summaries(text_analytics_client)
else:
    print("Authentication failed. Check your credentials.")
