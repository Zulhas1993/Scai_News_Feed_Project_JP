import os
import json
from datetime import datetime
from langchain.callbacks.manager import get_openai_callback
from langchain_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from Open_AI_Article_Create_Chat_API import get_news_details_list

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


def analysis_and_recommendation():
    request_messages = [SystemMessage(content="Please answer in English")]

    articles_dict = {}  # To store the generated articles
    current_id = 1000  # Starting Id

    news_details_list = get_news_details_list()

    for details_feed in news_details_list:
        try:
            if isinstance(details_feed, dict):
                current_id += 1  # Increment Id for each article

                news_entry = NewsFeed(
                    feed_id=current_id,  # Use feed_id instead of id
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

                # Generate article using Chat AI
                response = __call_chat_api(request_messages)
                content_from_api = response.content if isinstance(response, AIMessage) else str(response)
                created_article = str(content_from_api)

                # Extend request_messages to include the message about creating an article
                request_messages.extend([
                    AIMessage(content=created_article),
                    HumanMessage(content=f"Create Summary article for each details news , if any link or details news have a problem to creating article you skip the details news and continue for next details news and Create article one by one and all article will be within 150 words and response format is Title: , Link: ,Article  :\n{json.dumps(news_dict, ensure_ascii=False)}")
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
                
                # Convert news_dict to a JSON-formatted dictionary with the extracted article
                current_date = datetime.now().strftime("%Y-%m-%d")
                article_dict = {
                    'CurrentDate': current_date,  
                    'title': news_dict.get('title', ''),
                    'link': news_dict.get('ex_link', ''),
                    'detailsNews': news_dict.get('details_news', ''),  # Corrected key
                    'article': article_text  # Use extracted article_text as the article content
                }

                # Add the article to the dictionary with the current_id as the key
                articles_dict[current_id] = article_dict

            else:
                print("Warning: details_feed is not a dictionary.")

        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    # Print the response as JSON format
    print(json.dumps(articles_dict, ensure_ascii=False, indent=2))

# Call the analysis_and_recommendation function
analysis_and_recommendation()
