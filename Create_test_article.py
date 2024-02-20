import os
import json
from datetime import datetime
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from Details_News import get_news_details_list

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

def generate_article_details(news_entries, initial_feed_id):
    # Convert the NewsFeed objects to dictionaries
    news_dicts = [news_entry.__dict__ for news_entry in news_entries]

    articles_list = []
    print(f"loop:")
    for i, news_entry in enumerate(news_entries):
        # Initialize request_messages for the Chat AI
        request_messages = [SystemMessage(content="Please answer in English")]

        # Extend request_messages to include a message about creating an article
        request_messages.extend([
            HumanMessage(f"Create Summary article for the details news, if any link or details news has a problem creating an article, skip the details news and continue to the next details news. The response format is Title:, Link:, Article: \n{json.dumps(news_dicts[i], ensure_ascii=False)}")
        ])

        # print(request_messages)
        response_summary = __call_chat_api(request_messages)
        response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)

        request_messages.clear()

        # Extract the 'Article' part from response_summary_str
        article_start_index = response_summary_str.find('Article:')
        if article_start_index != -1:
            article_text = response_summary_str[article_start_index + len('Article:'):].strip()
        else:
            article_text = ""

        # Add Link, Title, Article, and Article ID to the list
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_article_id = initial_feed_id + i
        article_details = {
            'feed_id': initial_feed_id,
            'article_id': current_article_id,
            'Link': news_entry.ex_link,
            'title': news_entry.title,
            'article': article_text,  # Use the extracted article_text for each entry
            'date': current_date
        }
        articles_list.append(article_details)

    return articles_list

def get_articles_list():
    # Get news details list using the 'get_news_details_list' function
    news_details_list = get_news_details_list()
    #print(f"details_list :{news_details_list}")
    #print('details complete')
    # Starting Id for articles
    initial_feed_id = 100

    # Convert news details to NewsFeed objects
    news_entries = [NewsFeed(
        feed_id=details_feed.get('feed_id', 0),
        title=details_feed.get('title', ''),
        ex_link=details_feed.get('link', ''),
        details_news=details_feed.get('content', '')
    ) for details_feed in news_details_list.get('details_list', []) if isinstance(details_feed, dict)]
    print(f"news entries{news_entries}")
    # Process news entries one by one
    generated_articles_list = generate_article_details(news_entries, initial_feed_id)
    print(f"articles_list{generated_articles_list}")
    # Save generated_articles_list to a text file
    file_name = "articles_list.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json.dumps(generated_articles_list, ensure_ascii=False, indent=2))

    print("Articles list saved to:", file_name)

# Call the function to generate articles and save to a text file
get_articles_list()
