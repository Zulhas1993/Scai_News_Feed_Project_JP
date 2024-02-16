import os
import json
from datetime import datetime
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from component.Details_News import get_news_details_list

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

# Custom exception class for handling fetch details errors
class FetchDetailsError(Exception):
    pass

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    
    with get_openai_callback():
        return model(messages)

class NewsFeed:
    def __init__(self, feed_id, title, ex_link, details_news):
        self.feed_id = feed_id
        self.title = title
        self.ex_link = ex_link
        self.details_news = details_news

def get_articles_list():
    # Initialize a list to store the generated articles
    articles_list = []

    # Starting Id for articles
    current_feed_id = 100
    current_article_id = 0

    # Get news details list using the 'get_news_details_list' function
    news_details_list = get_news_details_list()

    # Iterate through each news details entry
    for details_feed in news_details_list:
        try:
            # Check if the entry is a dictionary
            if isinstance(details_feed, dict):
                # Increment Id for each article
                current_feed_id += 1
                current_article_id += 1

                # Create a NewsFeed object from details_feed
                news_entry = NewsFeed(
                    feed_id=current_feed_id,
                    title=details_feed.get('title', ''),
                    ex_link=details_feed.get('link', ''),
                    details_news=details_feed.get('details_news', '')
                )

                # Convert the NewsFeed object to a dictionary
                news_dict = news_entry.__dict__

                # Create a new request_messages list for each iteration
                request_messages = [SystemMessage(content="Please answer in English")]

                # Extend request_messages to include a message about creating an article
                request_messages.extend([
                    HumanMessage(f"Create Summary article for each details news, if any link or details news have a problem creating an article, skip the details news and continue for the next details news. Create articles one by one, and all articles will be within 150 words. The response format is Title:, Link:, Article: \n{json.dumps(news_dict, ensure_ascii=False)}")
                ])

                # Generate summary using Chat AI
                response_summary = __call_chat_api(request_messages)
                response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)

                # Extract the 'Article' part from response_summary_str
                article_start_index = response_summary_str.find('Article:')
                if article_start_index != -1:
                    article_text = response_summary_str[article_start_index + len('Article:'):].strip()
                else:
                    article_text = ""

                # Add Link, Title, Article, and Article ID to the list
                current_date = datetime.now().strftime("%Y-%m-%d")
                articles_list.append({
                    'feed_id': news_entry.feed_id,
                    'article_id': current_article_id,
                    'Link': news_dict.get('ex_link', ''),
                    'title': news_dict.get('title', ''),
                    'article': article_text,
                    'date': current_date
                })

            else:
                print("Warning: details_feed is not a dictionary.")

        except Exception as e:
            # Handle errors that occur during the generation of articles
            print(f"An error occurred: {e}")
            continue

    # Return the list of generated articles
    return articles_list

# Call the function and print the result
generated_articles_list = get_articles_list()

# Print the result to a text file
output_file_path = "generated_articles.txt"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(json.dumps(generated_articles_list, ensure_ascii=False, indent=2))

print(f"Results saved to {output_file_path}")


