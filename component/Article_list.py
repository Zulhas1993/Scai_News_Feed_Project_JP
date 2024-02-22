import os
import json
import time
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

# Initialize current IDs outside the functions
current_feed_id = 0
current_article_id = 0

def truncate_text(text, max_words):
    words = text.split()
    truncated_text = ' '.join(words[:max_words])
    return truncated_text

created_articles = []
not_created_articles = []

def generate_article_details(news_entry):
    # Use global keyword to modify global variables
    global current_feed_id
    global current_article_id

    # Increment feed_id for each news entry
    current_feed_id += 1
    current_article_id += 1

    # Initialize request_messages for the Chat AI
    request_messages = [SystemMessage(content="Please answer in English")]

    # Filter out sensitive content from individual news entry
    news_entry_content = {'content': news_entry.details_news}

    # Extend request_messages to include a message about creating an article
    request_messages.extend([
        HumanMessage(f"Create Summary article for the news entry within 150 words "
                     f"and in the Summary article there will be only article text :\n"
                     f"{json.dumps(news_entry_content, ensure_ascii=False)}")
    ])

    try:
        response_summary = __call_chat_api(request_messages)
        response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(
            response_summary)
    except ValueError as e:
        # Handle Azure content filter triggering error
        print(f"Azure Content Filter Triggered: {e}")
        response_summary_str = ""

    # Extract the 'Article' part from response_summary_str
    #article_text = response_summary_str.strip()
    article_text = truncate_text(response_summary_str.strip(), 150)

    # Add Link, Title, Article, and Article ID to the list
    current_date = datetime.now().strftime("%Y-%m-%d")

    article_details = {
        'feed_id': current_feed_id,
        'article_id': current_article_id,
        'Link': news_entry.ex_link,
        'title': news_entry.title,
        'article': article_text,
        'date': current_date
    }
    if article_text:
        # Article was created
        created_articles.append(article_details)
    else:
        # Article was not created
        not_created_articles.append(news_entry.ex_link)  # Store the link instead

    return article_details

def generate_article_details_chunked(news_entries):
    # Convert the NewsFeed objects to dictionaries
    news_dicts = [news_entry.__dict__ for news_entry in news_entries]
    chunk_size = 1
    articles_list = []
    print("Loop:")
    count = 1
    for i in range(0, len(news_dicts), chunk_size):
        if count > 10:
            break
        else:
            count += 1
        chunk = news_dicts[i:i + chunk_size]
        tem_count = 0  # Reset tem_count for each chunk
        print(i)
        # Process each news entry in the chunk
        for news_dict in chunk:
            
            article_details = generate_article_details(
                NewsFeed(
                    feed_id=news_dict['feed_id'],
                    title=news_dict['title'],
                    ex_link=news_dict['ex_link'],
                    details_news=news_dict['details_news']
                ),
            )

            articles_list.append(article_details)
            tem_count += 1  # Increment the counter for each news entry

    return articles_list

def get_articles_list():
    # Get news details list using the 'get_news_details_list' function
    news_details_list = get_news_details_list()

    # Convert news details to NewsFeed objects
    news_entries = [NewsFeed(
        feed_id=details_feed.get('feed_id', 0),
        title=details_feed.get('title', ''),
        ex_link=details_feed.get('link', ''),
        details_news=details_feed.get('content', '')
    ) for details_feed in news_details_list.get('details_list', []) if isinstance(details_feed, dict)]

    total_links = len(news_entries)
    print(f"Total Links: {total_links}")

    generated_articles_list = generate_article_details_chunked(news_entries)
    print(f"articles_list{generated_articles_list}")

    # Save generated_articles_list to a text file
    file_name = "articles_list.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(json.dumps(generated_articles_list, ensure_ascii=False, indent=2))

    # Save links for which articles were not created to a separate file
    not_created_file_name = "not_created_articles.txt"
    with open(not_created_file_name, 'w', encoding='utf-8') as not_created_file:
        not_created_file.write(json.dumps(not_created_articles, ensure_ascii=False, indent=2))

    print("Articles list saved to:", file_name)
    print("Not created articles list saved to:", not_created_file_name)

# Call the function to generate articles and save to a text file
get_articles_list()
