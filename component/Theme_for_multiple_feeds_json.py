import json
from datetime import datetime
from News_Feed_Json import News_Feed_Json_Return
from html import unescape

class ThemeInfo:
    def __init__(self, feed_Id, Theme_Id, Theme_title, article, date):
        self.feed_Id = feed_Id
        self.Theme_Id = Theme_Id
        self.Theme_title = Theme_title
        self.article = article
        self.date = date

def decode_title(title):
    return unescape(title)

# Store the current Theme_Id outside the function
current_theme_id = 1

def get_multiple_feed_for_theme(news_feed_data):
    global current_theme_id

    result_dict = {}

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
   
    for feed_id, data in news_feed_data.items():
        Theme_Id = f"Theme_Id_{current_theme_id}"
        feed_Id = f"feed_Id_{feed_id}"

        # Increment the counter for the next iteration
        #current_theme_id += 1

        # Decode and unescape the title
        decoded_title = decode_title(data["title"])

        # Check if the Theme_Id is already in the result_dict
        if Theme_Id not in result_dict:
            result_dict[Theme_Id] = {} 

        
        # Add a new entry for each feed_Id under the current Theme_Id
        result_dict[Theme_Id][feed_Id] = {
            "Title": decoded_title,
            "Link": data["link"],
            "Article": data["article"]
        }
        
    # Create the final result with the current date
    final_result = {current_date: result_dict}
    return json.dumps(final_result, indent=2, ensure_ascii=False)

# Assuming that News_Feed_Json_Return() returns a dictionary
news_feed_data = News_Feed_Json_Return()

result_json = get_multiple_feed_for_theme(news_feed_data)
print(result_json)
