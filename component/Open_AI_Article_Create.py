import json
import requests
import html2text
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from bs4 import BeautifulSoup
import re
from Details_News import generate_news_feed_list
class FetchDetailsError(Exception):
    pass


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

def authenticate_client():
    endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
    key = "09b7c88cfff44bac95c83a2256f31907"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def extract_news_info(data):
    news_list = []
    unique_links = set()  

    for key, value in data.items():
        for entry in value.values():
            entry_data = json.loads(entry)
            title = entry_data.get('title', '')
            link = entry_data.get('link', '')
            description = entry_data.get('description', '')
            subjectList = entry_data.get('subjectList', [])

            # Check if the link is not a duplicate and has details
            if link not in unique_links and description:
                news_list.append({'title': title, 'link': link, 'description': description, 'subjectList': subjectList})
                unique_links.add(link)
               
    return news_list

def get_news_details(link):
    try:
        # You can customize this function to fetch news details from the provided link
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
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

        return news_details_list

    except Exception as e:
        print(f"An error occurred during news details retrieval: {e}")
        return None

def remove_unnecessary_text(details_feed):
    cleaned_details_feed = re.sub(r'<.*?>', '', details_feed)
    cleaned_details_feed = re.sub(r'^\s*(?:unwanted1|unwanted2|unwanted3).*$', '', cleaned_details_feed, flags=re.MULTILINE)
    keywords_to_remove = ['unwanted1', 'unwanted2', 'unwanted3', 'image', 'picture', 'photo']
    for keyword in keywords_to_remove:
        cleaned_details_feed = re.sub(fr'\b{keyword}\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    cleaned_details_feed = re.sub(r'\b(?:ad|advertisement|promo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    cleaned_details_feed = re.sub(r'\b(?:image|picture|photo)\b.*$', '', cleaned_details_feed, flags=re.IGNORECASE | re.MULTILINE)
    cleaned_details_feed = re.sub(r'\s+', ' ', cleaned_details_feed).strip()
    return cleaned_details_feed

def format_news_details(details_feed):
    soup = BeautifulSoup(details_feed, 'html.parser')
    cleaned_details_feed = soup.get_text(separator=' ')
    cleaned_details_feed = ' '.join(cleaned_details_feed.split())
    return cleaned_details_feed


def generate_abstractive_summary(text_analytics_client, document, language='en'):
    try:
        poller = text_analytics_client.begin_abstract_summary([document])
        abstract_summary_results = poller.result()
        
        for result in abstract_summary_results:
            if result.kind == "AbstractiveSummarization":
                print("Summaries abstracted:")
                return [summary.text for summary in result.summaries]
            elif result.is_error is True:
                print(f"Error in abstractive summarization: Code {result.error.code}, Message {result.error.message}")
                return None

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        raise  # Re-raise the exception to provide more information in the main exception handler


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

import json

def generate_abstractive_summaries(text_analytics_client):
    try:
        all_summaries_dict = {}
        news_details_list = generate_news_feed_list()  # Replace with the correct import

        for idx, news_feed in enumerate(news_details_list, start=1):
            if not isinstance(news_feed, dict):
                print(f"Warning: news_feed at index {idx} is not a dictionary. Details: {news_feed}")
                continue

            # Ensure that 'details_news' is present
            if 'details_news' not in news_feed:
                print(f"Warning: news_feed at index {idx} does not have 'details_news'. Details: {news_feed}")
                continue

            # Make 'details_news' a valid dictionary if it's not
            news_feed['details_news'] = make_details_news_valid(news_feed['details_news'])

            # Rest of your processing code for valid dictionaries
            cleaned_details_feed = remove_unnecessary_text(news_feed['details_news'])
            formatted_details_feed = format_news_details(cleaned_details_feed)

            source_link = news_feed.get('link', '')
            article = create_article(formatted_details_feed, source_link)
            summaries = generate_abstractive_summary(text_analytics_client, formatted_details_feed)

            all_summaries_dict[news_feed['date']] = {
                'id': news_feed.get('id', ''),
                'title': news_feed.get('title', ''),
                'link': source_link,
                'article': article,  # Include the generated article
                'summaries': summaries
            }

        # Write the dictionary to a JSON file with proper encoding
        output_file_path = 'summaries_output.json'
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_summaries_dict, json_file, ensure_ascii=False, indent=2)

        print(f"Summaries have been written to {output_file_path}")
        return all_summaries_dict

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return None





# Authenticate the Text Analytics client
text_analytics_client = authenticate_client()

# Generate abstractive summaries
all_summaries_dict = generate_abstractive_summaries(text_analytics_client)

# Check if summaries were generated successfully
if all_summaries_dict is not None:
    # Write the dictionary to a JSON file
    output_file_path = 'summaries_output.json'
    try:
        with open(output_file_path, 'w', encoding='utf-16') as json_file:
            json.dump(all_summaries_dict, json_file, ensure_ascii=False, indent=2)
        print(f"Summaries have been written to {output_file_path}")
    except Exception as e:
        print(f"An error occurred while writing summaries to JSON file: {e}")
else:
    print("Abstractive summaries generation failed. Check previous error messages for details.")

