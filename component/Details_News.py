import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from docx import Document
import traceback
from datetime import datetime
from html import unescape
class FetchDetailsError(Exception):
    pass

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
        print(f"Response Status Code: {response.status_code}")
        response.raise_for_status()  
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

def generate_news_feed_list():
    try:
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)

        # Extract news information
        news_list = extract_news_info(data)
        news_feed_list = []

        # Initialize ID to 1
        current_id = 1

        for news in news_list:
            link = news.get('link', '')
            try:
                # Fetch details for each link
                news_details = get_news_details(link)

                if news_details:
                    # Create an instance of NewsFeed with a unique ID and append it to the list
                    news_feed = NewsFeed(
                        id=current_id,
                        title=news.get('title', ''),
                        tags=[],
                        ex_link=link,
                        description=news.get('description', ''),
                        details_news=news_details.get('content', ''),
                        keywords=[],
                        article=None,
                        date=None
                    )
                    news_feed_list.append(news_feed)

                    # Increment ID for the next instance
                    current_id += 1

            except FetchDetailsError as e:
                print(f"An error occurred while fetching details for link: {link}. {str(e)}")
                traceback.print_exc()  # Print the traceback for the exception

        # Serialize the list of NewsFeed instances to JSON
        #news_feed_json = json.dumps([news_feed.__dict__ for news_feed in news_feed_list], indent=2)

        return news_feed_list

    except Exception as e:
        print(f"An error occurred during news feed generation: {e}")
        traceback.print_exc()  # Print the traceback for the exception
        return None

# Generate news feed list in JSON format
generated_news_feed_json = generate_news_feed_list()

# Print or save the generated JSON string

# if generated_news_feed_json:
#     print(generated_news_feed_json)


# def save_news_feed_to_docx(news_feed_list):
#     try:
#         doc = Document()

#         for news_feed in news_feed_list:
#             doc.add_heading(news_feed.title, level=1)
#             doc.add_paragraph(f"ID: {news_feed.id}")
#             doc.add_paragraph(f"Title: {news_feed.title}")
#             doc.add_paragraph(f"Tags: {', '.join(news_feed.tags)}")
#             doc.add_paragraph(f"External Link: {news_feed.ex_link}")
#             doc.add_paragraph(f"Description: {news_feed.description}")
#             doc.add_paragraph(f"Details News: {news_feed.details_news}")
#             doc.add_paragraph(f"Keywords: {', '.join(news_feed.keywords)}")
#             doc.add_paragraph(f"Article: {news_feed.article}")
#             doc.add_paragraph(f"Date: {news_feed.date}")
#             doc.add_page_break()

#         doc.save('news_feed_details.docx')
#         print("News feed details saved to news_feed_details.docx")

#     except Exception as e:
#         print(f"An error occurred while saving news feed to DOCX: {e}")

# # Save NewsFeed instances to DOCX
# if generated_news_feed_json:
#     save_news_feed_to_docx(generated_news_feed_json)




def generate_date_wise_news_feed_list():
    try:
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)
        current_id = 1
        # Extract news information
        news_list = extract_news_info(data)
        news_feed_list = {}

        for news in news_list:
            link = news.get('link', '')
            try:
                # Fetch details for each link
                news_details = get_news_details(link)

                if news_details:
                    # Create a dictionary with necessary details
                    news_feed_dict = {
                        "Id": current_id,
                        "Title": unescape(news.get('title', '')),  # Decode Unicode escape sequences in the title
                        "Link": link,
                        "Description": news.get('description', ''),
                    }

                    # Get the current date
                    current_date = datetime.now().strftime("%Y-%m-%d")

                    # Append the dictionary to the news_feed_list using the date as the key
                    news_feed_list.setdefault(current_date, []).append(news_feed_dict)

                    # Increment ID for the next instance
                    current_id += 1

            except FetchDetailsError as e:
                traceback.print_exc()  # Print the traceback for the exception

        # Serialize the news_feed_list dictionary to JSON with readable or decoded data
        news_feed_json = json.dumps(news_feed_list, ensure_ascii=False, indent=2)

        return news_feed_json

    except Exception as e:
        traceback.print_exc()  # Print the traceback for the exception
        return None

# Call the function and print the result
generated_date_wise_news_feed_json = generate_date_wise_news_feed_list()
print(generated_date_wise_news_feed_json)

def save_date_wise_news_feed_to_docx(news_feed_json):
    try:
        doc = Document()

        # Load the JSON data
        news_feed_data = json.loads(news_feed_json)

        for date, news_list in news_feed_data.items():
            doc.add_heading(f"Date: {date}", level=1)
            for news_feed in news_list:
                doc.add_paragraph(f"ID: {news_feed['Id']}")
                doc.add_paragraph(f"Title: {news_feed['Title']}")
                doc.add_paragraph(f"Link: {news_feed['Link']}")
                doc.add_paragraph(f"Description: {news_feed['Description']}")
                doc.add_page_break()

        doc.save('date_wise_news_feed.docx')
        print("News feed details saved to date_wise_news_feed.docx")

    except Exception as e:
        print(f"An error occurred while saving news feed to DOCX: {e}")

# Call the function and pass the generated JSON
if generated_date_wise_news_feed_json:
    save_date_wise_news_feed_to_docx(generated_date_wise_news_feed_json)













