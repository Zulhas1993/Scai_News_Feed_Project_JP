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
        # Initialize a dictionary to store the summaries
        all_summaries_dict = {}

        news_details_list = generate_news_feed_list()

        for idx, news_feed in enumerate(news_details_list, start=1):
            # Accessing details_news attribute
            details = news_feed.details_news if hasattr(news_feed, 'details_news') else ''
            # Generate abstractive summaries for each news article
            summaries = generate_abstractive_summary(text_analytics_client, details)
            #current_date = datetime.now().strftime("%Y-%m-%d")
            # Append the summaries to the dictionary
            all_summaries_dict[news_feed.date] = {
                'id': news_feed.id,
                'title': news_feed.title,
                'link': news_feed.ex_link,
                #'details': details,
                'summaries': summaries
            }

        return all_summaries_dict

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        return None

def generate_abstractive_summary(text_analytics_client, document, language='en'):
    try:
        poller = text_analytics_client.begin_abstract_summary([document])  # Pass document as a list
        abstract_summary_results = poller.result()
        for result in abstract_summary_results:
            if result.kind == "AbstractiveSummarization":
                print("Summaries abstracted:")
                [print(f"{summary.text}\n") for summary in result.summaries]
            elif result.is_error is True:
                print("...Is an error with code '{}' and message '{}'".format(
                    result.error.code, result.error.message
                ))

    except Exception as e:
        print(f"An error occurred during abstractive summarization: {e}")
        raise  # Re-raise the exception to provide more information in the main exception handler


# Authenticate the Text Analytics client
text_analytics_client = authenticate_client()

# Generate abstractive summaries
all_summaries_dict = generate_abstractive_summaries(text_analytics_client)

# Write the dictionary to a JSON file
output_file_path = 'summaries_output.json'
with open(output_file_path, 'w', encoding='utf-16') as json_file:
    json.dump(all_summaries_dict, json_file, ensure_ascii=False, indent=2)

print(f"Summaries have been written to {output_file_path}")
