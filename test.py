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

def generate_article_details(news_entry, current_article_id, current_feed_id):
    request_messages = [
        SystemMessage(content="Please answer in English"),
        HumanMessage(f"Create Summary article for the news entry within 150 words And Title text will be remove from the Article text:\n{json.dumps(news_entry.__dict__, ensure_ascii=False)}")
    ]

    response_summary = __call_chat_api(request_messages)
    response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(response_summary)

    article_start_index = response_summary_str.find('Article:')
    article_text = response_summary_str[article_start_index + len('Article:'):].strip() if article_start_index != -1 else ""

    current_date = datetime.now().strftime("%Y-%m-%d")
    
    article_details = {
        'feed_id': current_feed_id,
        'article_id': current_article_id,
        'Link': news_entry.ex_link,
        'title': news_entry.title,
        'article': article_text,
        'date': current_date
    }

    return article_details

def generate_article_details_chunked(news_entries, initial_feed_id):
    articles_list = []
    count = 1

    for news_entry in news_entries:
        if count > 10:
            break

        # Process each news entry
        article_details = generate_article_details(news_entry, initial_feed_id, initial_feed_id)
        articles_list.append(article_details)

        # Increment the counter and overall counter for each news entry
        initial_feed_id += 1
        count += 1

    return articles_list

def get_articles_list():
    news_details_list = get_news_details_list()
    initial_feed_id = 0

    news_entries = [NewsFeed(
        feed_id=details_feed.get('feed_id', 0),
        title=details_feed.get('title', ''),
        ex_link=details_feed.get('link', ''),
        details_news=details_feed.get('content', '')
    ) for details_feed in news_details_list.get('details_list', []) if isinstance(details_feed, dict)]

    total_links = len(news_entries)
    print(f"Total Links: {total_links}")

    generated_articles_list = []
    links_cannot_create_article = []

    # Limit the loop to create only 10 articles for testing
    # for i, news_entry in enumerate(news_entries, start=1):
    for i, news_entry in enumerate(news_entries[:10], start=1):
        try:
            article_details = generate_article_details(news_entry, initial_feed_id + i, initial_feed_id)
            generated_articles_list.append(article_details)
            print(f"Article created for Link {i}/{10}")  # Displaying progress for the first 10 articles
        except Exception as e:
            # Handle any exceptions during article creation
            links_cannot_create_article.append(news_entry.ex_link)
            print(f"Error creating article for Link {i}/{10}: {e}")

    file_name = "articles_list_test.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        for article_details in generated_articles_list:
            # Remove "Title" and "Summary" parts
            article_details.pop('title', None)
            article_details.pop('summary', None)
            file.write(json.dumps(article_details, ensure_ascii=False, indent=2))
            file.write("\n")

    print("Articles list saved to:", file_name)

    if links_cannot_create_article:
        print("\nLinks for which articles could not be created:")
        for link in links_cannot_create_article:
            print(link)

get_articles_list()

