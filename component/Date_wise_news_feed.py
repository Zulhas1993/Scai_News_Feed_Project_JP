import json
from datetime import datetime
import traceback
from html import unescape
from Details_News import extract_news_info, get_news_details

class FetchDetailsError(Exception):
    pass

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

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
                details_news = news_details.get('content', '')

                if news_details:
                    # Create a dictionary with necessary details
                    news_feed_dict = {
                        "Id": current_id,
                        "Title": unescape(news.get('title', '')),  # Decode Unicode escape sequences in the title
                        "Link": link,
                        "Description": news.get('description', ''),
                        "News Details":details_news,
                        
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
        print(news_feed_json)
        return news_feed_json

    except Exception as e:
        traceback.print_exc()  # Print the traceback for the exception
        return None

# Call the function and print the result
generated_date_wise_news_feed_json = generate_date_wise_news_feed_list()
print("Generated JSON:", generated_date_wise_news_feed_json)
