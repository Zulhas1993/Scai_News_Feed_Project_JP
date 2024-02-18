import json
import traceback
from datetime import datetime
from html import unescape
from requests.exceptions import SSLError
from Scrapping_Feeds import fillDictionaryWithData,get_all_links
from  Details_News import get_news_details

class FetchDetailsError(Exception):
    pass

def generate_date_wise_news_feed_list():
    try:
        # Assuming these functions are defined somewhere
        Data = fillDictionaryWithData()
        scrapping_data = get_all_links(Data)

        # Ensure scrapping_data is a list of dictionaries
        if not isinstance(scrapping_data, list) or not all(isinstance(item, dict) for item in scrapping_data):
            raise ValueError("Invalid data format. Expected a list of dictionaries.")

        current_id = 1
        news_feed_list = {}

        for news in scrapping_data:
            link = news.get('link', '')
            try:
                news_details = get_news_details(link)
                details_news = news_details.get('content', '')

                if news_details:
                    news_feed_dict = {
                        "Id": current_id,
                        "Title": unescape(news.get('title', '')),
                        "Link": link,
                        "Description": news.get('description', ''),
                        "News Details": details_news,
                    }

                    current_date = datetime.now().strftime("%Y-%m-%d")
                    news_feed_list.setdefault(current_date, []).append(news_feed_dict)
                    current_id += 1

            except FetchDetailsError as e:
                traceback.print_exc()

            except SSLError as e:
                print(f"SSL Error for link {link}: {str(e)}")
                # Handle SSL error, log it, or continue with the next link

        news_feed_json = json.dumps(news_feed_list, ensure_ascii=False, indent=2)

        # Save the response in a text file with .txt extension
        file_name = "date_wise_news_feed.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(news_feed_json)

        return news_feed_json

    except Exception as e:
        traceback.print_exc()
        return None

# Call the function and print the result
generated_date_wise_news_feed_json = generate_date_wise_news_feed_list()
#print("Generated JSON:", generated_date_wise_news_feed_json)
