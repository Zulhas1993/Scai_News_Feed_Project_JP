import json
import traceback
from datetime import datetime
from html import unescape
from Scrapping_Feeds import fillDictionaryWithData,get_all_links
from  Details_News import get_news_details
import requests

class FetchDetailsError(Exception):
    pass

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

import time

def generate_date_wise_news_feed_list():
    try:
        Data = fillDictionaryWithData()
        scrapping_data = get_all_links(Data)

        if not isinstance(scrapping_data, list) or not all(isinstance(item, dict) for item in scrapping_data):
            raise ValueError("Invalid data format. Expected a list of dictionaries.")

        current_id = 1
        news_feed_list = {}
        error_links = []

        for news in scrapping_data:
            link = news.get('link', '')
            try:
                start_time = time.time()  # Record start time

                news_details = get_news_details(link)

                if news_details is None:
                    print(f"Skipping link due to NoneType news_details: {link}")
                    error_links.append(link)
                    continue  # Continue to the next iteration of the loop

                details_news = news_details.get('content', '')

                if details_news:
                    news_feed_dict = {
                        "Id": current_id,
                        "Title": unescape(news.get('title', '')),
                        "Link": link,
                        "Description": news.get('description', ''),
                        "News Details": details_news,
                        "Execution Time": time.time() - start_time  # Calculate execution time
                    }

                    current_date = datetime.now().strftime("%Y-%m-%d")
                    news_feed_list.setdefault(current_date, []).append(news_feed_dict)
                    current_id += 1

            except FetchDetailsError as e:
                print(f"Error for link: {link}. {str(e)}")
                error_links.append(link)
                continue  # Continue to the next iteration of the loop

        if error_links:
            print("Links with errors:", error_links)

        # Convert the dictionary to a JSON string
        news_feed_json = json.dumps(news_feed_list, ensure_ascii=False, indent=2)

        file_name = "date_wise_news_feed.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(news_feed_json)

        return news_feed_json, error_links

    except Exception as e:
        traceback.print_exc()
        return None

# Call the function and print the result
generated_date_wise_news_feed_json, error_links = generate_date_wise_news_feed_list()
# print("Generated JSON:", generated_date_wise_news_feed_json)
# print("Error Links:", error_links)




