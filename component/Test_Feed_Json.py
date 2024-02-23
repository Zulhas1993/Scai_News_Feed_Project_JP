import json
from datetime import datetime
from langchain.callbacks.manager import get_openai_callback
from Details_News import get_news_details_list
from test_articles import get_articles_list


# Custom exception class for handling fetch details errors
class FetchDetailsError(Exception):
    pass

class NewsFeed:
    def __init__(self, feed_id, title, tags, ex_link, description, details_news, keywords, article, date):
        self.feed_id = feed_id
        self.title = title
        self.tags = tags
        self.ex_link = ex_link
        self.description = description
        self.details_news = details_news
        self.keywords = keywords
        self.article = article
        self.date = date


def News_Feed_Json_Return():
    articles_dict = {}  
    current_id = 100  
    news_details_list = get_news_details_list()

    # Get the articles list
    articles_list = get_articles_list()

    for index, details_feed in enumerate(news_details_list, start=current_id):
        try:
            if isinstance(details_feed, dict):
                current_id += 1 

                news_entry = NewsFeed(
                    feed_id=current_id,
                    title=details_feed.get('title', ''),
                    tags="",
                    ex_link=details_feed.get('link', ''),
                    description="",
                    details_news=details_feed.get('details_news', ''),
                    keywords="",
                    article="",
                    date=""
                )

                news_dict = news_entry.__dict__

                # Find the corresponding article in the articles_list based on link
                matching_article = next((article for article in articles_list if article.get("Link") == news_dict.get('ex_link')), None)

                if matching_article:
                    # Convert news_dict to a JSON-formatted dictionary with the extracted article
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    article_dict = {
                        'CurrentDate': current_date,
                        'title': news_dict.get('title', ''),
                        'link': news_dict.get('ex_link', ''),
                        'detailsNews': news_dict.get('details_news', ''),
                        'article': matching_article.get("article", "")
                    }

                    # Add the article to the dictionary with the current_id as the key
                    articles_dict[current_id] = article_dict
                else:
                    print(f"Warning: No matching article found for link {news_dict.get('ex_link')}")

            else:
                print(f"Warning: Element at index {index} in news_details_list is not a dictionary.")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    # Return the generated articles dictionary
    return articles_dict

# Call the News_Feed_Json_Return function and capture the response
generated_articles = News_Feed_Json_Return()

# Print the response as JSON format
print(json.dumps(generated_articles, ensure_ascii=False, indent=2))




