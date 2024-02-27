import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from docx import Document
import traceback
from datetime import datetime
from html import unescape
import html2text
import newspaper
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from Scrapping_Feeds import fillDictionaryWithData,get_all_links
class FetchDetailsError(Exception):
    pass


def authenticate_client():
    endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
    key = "09b7c88cfff44bac95c83a2256f31907"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

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

    # Use a set to keep track of unique links to avoid duplicates
    unique_links = set()

    # Iterate through the list of dictionaries
    for entry_data in data:
        # Print the raw entry data
        #print("Raw Entry Data:", entry_data)

        # Extract relevant information from the entry data
        title = entry_data.get('title', '')
        link = entry_data.get('link', '')
        description = entry_data.get('description', '')
        tags = entry_data.get('tags', {})
        subjectList = list(tags.values())

        # Print the extracted information
        #print("Extracted Info:", {'title': title, 'link': link, 'description': description, 'subjectList': subjectList})

        # Check if the link is not a duplicate and has a description
        if link not in unique_links and description:
            # Append the extracted information to the news_list
            news_list.append({'title': title, 'link': link, 'description': description, 'subjectList': subjectList})
            
            # Add the link to the set to mark it as seen
            unique_links.add(link)

    # Return the list of extracted news information
    return news_list
    # use newspaper
def get_news_details(link):
    try:
        
        article = newspaper.Article(link)
        article.download()
        article.parse()

        # Check if the article text is not empty or contains only whitespace
        if article.text and not article.text.isspace():
            # Return the news details
            return {'content': article.text.strip()}
        else:
            # Return None if there are no details
            return None
    except Exception as e:
        #print(f"Error fetching details for link: {link}. {str(e)}")
        return None

# def get_news_details(link):
#     try:
#         # You can customize this function to fetch news details from the provided link
#         response = requests.get(link)
#         # print(f"Response Status Code: {response.status_code}")
#         # response.raise_for_status()  
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Use html2text to convert HTML content to plain text
#         details_text = html2text.html2text(soup.get_text())

#         # Check if the details_text is not empty or contains only whitespace
#         if details_text and not details_text.isspace():
#             # Return the news details
#             return {'content': details_text.strip()}
#         else:
#             # Return None if there are no details
#             return None
#     except requests.RequestException as e:
#         pass
        

def get_news_details_list():
   
    #print('Scraping start')

    try:
        # Retrieve data for scraping using the fillDictionaryWithData function
        Data = fillDictionaryWithData()

        # Scrape all links using the get_all_links function
        scrapping_data = get_all_links(Data)

        # Extract news information from the scraped data
        news_list = extract_news_info(scrapping_data)

        # Initialize empty lists to store news details and error links
        news_details_list = []
        error_links = []

        # Iterate through each news in the news_list
        for news in news_list:
            # Extract link from the news
            link = news.get('link', '')

            try:
                # Retrieve detailed news information using the get_news_details function
                news_details = get_news_details(link)

                # If news_details is None, continue to the next iteration
                if news_details is None:
                    continue

                # Extract relevant details from news_details
                details_content = news_details.get('content', '')
                title = unescape(news.get('title', ''))
                description = (news.get('description'), '')

                # If details_content is not empty, add news details to the news_details_list
                if details_content:
                    news_details_list.append({'link': link, 'content': details_content, 'title': title, 'description': description})

            except FetchDetailsError as e:
                # If an exception (FetchDetailsError) occurs, add the link to the error_links list
                error_links.append(link)
                continue

        # Return a dictionary containing the details_list and error_links
        return {'details_list': news_details_list, 'error_links': error_links}

    except Exception as e:
        # Handle any general exceptions and print an error message
        print(f"An exception occurred: {e}")

        # Return a dictionary with None values if an exception occurs
        return {'details_list': None, 'error_links': None}


# details_result = get_news_details_list()
# details_list = details_result['details_list']
# error_links = details_result['error_links']

# print("Details list:", details_list)
# print("Error Links:", error_links)








# def get_news_details_list():
#     try:
#         Data = fillDictionaryWithData()
#         scrapping_data = get_all_links(Data)
#         news_list = extract_news_info(scrapping_data)
#         news_details_list = []
#         error_links = []

#         for news in news_list:
#             link = news.get('link', '')
#             try:
#                 news_details = get_news_details(link)
#                 if news_details is None:
#                     continue

#                 details_content = news_details.get('content', '')
#                 title = unescape(news.get('title', ''))

#                 if details_content:
#                     news_details_list.append({'link': link, 'content': details_content, 'title': title})
#             except FetchDetailsError as e:
#                 error_links.append(link)
#                 continue  

#         return news_details_list, error_links

#     except Exception as e:
#         print(f"An exception occurred: {e}")
#         return None, None

# details_list, error_links = get_news_details_list()

# # Save details_list to a text file
# file_name = "details_list.txt"
# with open(file_name, 'w', encoding='utf-8') as file:
#     for details in details_list:
#         file.write(f"Link: {details['link']}\nContent: {details['content']}\nTitle: {details['title']}\n\n")

# print("Details list saved to:", file_name)
# print("Error Links:", error_links)






# def generate_news_feed_list():
#     try:
#         file_path = 'object_list.json'

#         # Read JSON file
#         data = read_json(file_path)

#         # Extract news information
#         news_list = extract_news_info(data)
#         news_feed_list = []

#         # Initialize ID to 1
#         current_id = 1

#         for news in news_list:
#             link = news.get('link', '')
#             try:
#                 # Fetch details for each link
#                 news_details = get_news_details(link)
#                 details_news = news_details.get('content', '')

#                 if news_details:
#                     # Generate abstractive summaries
#                     text_analytics_client = authenticate_client()
                   
#                     # Create an instance of NewsFeed with a unique ID and append it to the list
#                     news_feed = NewsFeed(
#                         id=current_id,
#                         title=news.get('title', ''),
#                         tags=[],
#                         ex_link=link,
#                         description=news.get('description', ''),
#                         details_news=details_news,
#                         keywords=[],
#                         article=None,  # Update the 'article' attribute with generated summaries
#                         date=None
#                     )
#                     news_feed_list.append(news_feed)

#                     # Increment ID for the next instance
#                     current_id += 1

#             except FetchDetailsError as e:
#                 print(f"An error occurred while fetching details for link: {link}. {str(e)}")
#                 # traceback.print_exc()  # Print the traceback for the exception
#             #print(news_feed_list)
#         # Convert news_feed_list to JSON format
#         generated_news_feed_json = json.dumps([news_feed.__dict__ for news_feed in news_feed_list], default=str, ensure_ascii=False, indent=4)
#         #print(generated_news_feed_json)
#         return generated_news_feed_json

#     except Exception as e:
#         print(f"An error occurred during news feed generation: {e}")
#         # traceback.print_exc()  # Print the traceback for the exception
#         return None




# # Generate news feed list in JSON format
# generated_news_feed_json = generate_news_feed_list()



# def generate_date_wise_news_feed_list():
#     try:
#         file_path = 'object_list.json'

#         # Read JSON file
#         data = read_json(file_path)
#         current_id = 1
#         # Extract news information
#         news_list = extract_news_info(data)
#         news_feed_list = {}

#         for news in news_list:
#             link = news.get('link', '')
#             try:
#                 # Fetch details for each link
#                 news_details = get_news_details(link)

#                 if news_details:
#                     # Create a dictionary with necessary details
#                     news_feed_dict = {
#                         "Id": current_id,
#                         "Title": unescape(news.get('title', '')),  # Decode Unicode escape sequences in the title
#                         "Link": link,
#                         "Description": news.get('description', ''),
#                     }

#                     # Get the current date
#                     current_date = datetime.now().strftime("%Y-%m-%d")

#                     # Append the dictionary to the news_feed_list using the date as the key
#                     news_feed_list.setdefault(current_date, []).append(news_feed_dict)

#                     # Increment ID for the next instance
#                     current_id += 1

#             except FetchDetailsError as e:
#               traceback.print_exc()  # Print the traceback for the exception

#         # Serialize the news_feed_list dictionary to JSON with readable or decoded data
#         news_feed_json = json.dumps(news_feed_list, ensure_ascii=False, indent=2)

#         return news_feed_json

#     except Exception as e:
#         #traceback.print_exc()  # Print the traceback for the exception
#         return None

# # Call the function and print the result
# generated_date_wise_news_feed_json = generate_date_wise_news_feed_list()














