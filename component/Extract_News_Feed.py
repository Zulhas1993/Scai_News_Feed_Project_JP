import json
import requests
from bs4 import BeautifulSoup

class FetchDetailsError(Exception):
    pass

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data


def extract_news_info(data):
    news_list = []
    unique_links = set()  # Use a set to track unique links

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




# def get_news_details(link):
#     try:
#         # You can customize this function to fetch news details from the provided link
#         response = requests.get(link)
#         response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
#         soup = BeautifulSoup(response.text, 'html.parser')        
#         # Extract text content from the webpage
#         details_text = soup.get_text()
#         max_document_size = 5120  # Maximum allowed text elements
#         if len(details_text) > max_document_size:
#             details_text = details_text[:max_document_size]
            
#         # Return the news details
#         return {'content': details_text}
#     except requests.RequestException as e:
#         raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")



def get_news_details(link):
    try:
        # You can customize this function to fetch news details from the provided link
        response = requests.get(link)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        soup = BeautifulSoup(response.text, 'html.parser')        
        # Extract text content from the webpage
        details_text = soup.get_text()

        # Check if the details_text is not empty or contains only whitespace
        if details_text and not details_text.isspace():
            # Return the news details
            return {'content': details_text}
        else:
            # Return None if there are no details
            return None
    except requests.RequestException as e:
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")


def get_unique_links_with_count(news_list):
    links_count = {}  # Use a dictionary to store unique links and their counts
    for news in news_list:
        if 'content' in news:  # Check if the news has details
            link = news['link']
            # Increment the count for each occurrence of the link
            links_count[link] = links_count.get(link, 0) + 1

    return links_count
# Adjusted code
file_path = 'object_list.json'
data = read_json(file_path)    
news_list = extract_news_info(data)

for news in news_list:
    link = news['link']
    try:
        news_details = get_news_details(link)
        if news_details:
            # Add the fetched details to the news dictionary
            news.update(news_details)
    except FetchDetailsError as e:
        print(str(e))  # Handle or log the error as needed

unique_links_count = get_unique_links_with_count(news_list)

# Print only unique links with details and their counts
print("Unique links:")
for link, count in unique_links_count.items():
    print(link)

total_unique_links = len(unique_links_count)
print(f"Total unique links: {total_unique_links}")
