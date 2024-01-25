import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from Details_News import generate_news_feed_list

class FetchDetailsError(Exception):
    pass

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

def authenticate_client():
    endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
    key = "09b7c88cfff44bac95c83a2256f31907"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

class NewsFeed:
    def __init__(self, id, title, tags, ex_link, description, details_news, keywords, article, date):
        self.id = id
        self.title = title
        self.tags = tags
        self.ex_link = ex_link
        self.description = description
        self.details_news = details_news
        self.keywords = keywords
        self.article = article
        self.date = date

def generate_abstractive_summaries(text_analytics_client):
    try:
        # Initialize a list to store the summaries
        all_summaries = []

        news_details_list = generate_news_feed_list()

        for idx, news_feed in enumerate(news_details_list, start=1):
            # Accessing details_news attribute
            details = news_feed.details_news if hasattr(news_feed, 'details_news') else ''
            # Generate abstractive summaries for each news article
            summaries = generate_abstractive_summary(text_analytics_client, details)

            # Append the summaries to the list
            all_summaries.append({
                'article_number': idx,
                'title': news_feed.title,
                'link': news_feed.ex_link,
                'details': details,
                'summaries': summaries
            })

        return all_summaries

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return None


def generate_abstractive_summary(text_analytics_client, document_to_summarize):
    try:
        # Check if document text is empty
        if not document_to_summarize.strip():
            print("Document text is empty.")
            return []

        # Begin abstractive summarization
        poller = text_analytics_client.begin_abstract_summary(documents=[{"id": "1", "text": document_to_summarize}])
        abstract_summary_results = poller.result()

        summaries = []
        for result in abstract_summary_results:
            if result.kind == "AbstractiveSummarization":
                summaries.extend([summary.text for summary in result.summaries])
            elif result.is_error is True:
                print("An error occurred with code '{}' and message '{}'".format(
                    result.error.code, result.error.message
                ))

        return summaries

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return []

# Authenticate the Text Analytics client
text_analytics_client = authenticate_client()

# Generate abstractive summaries
all_summaries = generate_abstractive_summaries(text_analytics_client)

# Print the summaries
for summary in all_summaries:
    print(f"Article {summary['article_number']} - {summary['title']} - {summary['link']}")
    if summary['summaries']:
        for idx, s in enumerate(summary['summaries'], start=1):
            print(f"Summary {idx}: {s}")
    else:
        print("No summaries available.")
    print("\n")
