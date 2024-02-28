import os
import json,re
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
    def __init__(self, feed_id, title, ex_link, details_news, description):
        self.feed_id = feed_id
        self.title = title
        self.ex_link = ex_link
        self.details_news = details_news
        self.description = description

# Initialize current IDs outside the functions
current_feed_id = 0
current_article_id = 0


def truncate_text(text, max_words):
    # Split the input text into a list of words
    words = text.split()

    # Take only the first 'max_words' words from the list
    truncated_words = words[:max_words]

    # Join the truncated words back into a string
    truncated_text = ' '.join(truncated_words)

    # Define a regular expression pattern to identify sentence endings
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    # Split the truncated text into sentences using the sentence endings pattern
    sentences = re.split(sentence_endings, truncated_text)

    # Check if there is more than one sentence and the length exceeds the word limit
    if len(sentences) > 1 and len(' '.join(sentences[:-1])) > max_words:
        # Remove the last incomplete sentence if it exceeds the word limit
        sentences.pop()

    # Join the remaining sentences into the final truncated text
    return ' '.join(sentences)


created_articles = []
not_created_articles = []

def generate_article_details(news_entry):
    global current_feed_id
    global current_article_id

    current_feed_id += 1
    current_article_id += 1

    request_messages = [SystemMessage(content="Please answer in English")]

    news_entry_content = {'content': news_entry.details_news}

    request_messages.extend([
        HumanMessage(f"Create Summary article for the news entry within 150 words"
                     f"And There will be two part one is Title Of the Summary Article And another is Summary. Format is Title: ,Summary: :\n"
                     f"{json.dumps(news_entry_content, ensure_ascii=False)}")
    ])

    try:
        response_summary = __call_chat_api(request_messages)
        response_summary_str = response_summary.content if isinstance(response_summary, AIMessage) else str(
            response_summary)
    except ValueError as e:
        print(f"Azure Content Filter Triggered: {e}")
        response_summary_str = ""
        
    # Extracting the article text and removing the title
    #article_text = response_summary_str.strip().replace(news_entry.title, '')
    article_text = truncate_text(response_summary_str.strip(), 150)

    # title = article_text['article']['title']
    # summary = article_text['article']['Summary']

    # Find the indices of "Title:" and "Summary:" in the summary text
    title_index = article_text.find("Title:")
    summary_index = article_text.find("Summary:")

# Extract the title and summary based on the indices
    title = article_text[title_index + len("Title:"):summary_index].strip()
    summary = article_text[summary_index + len("Summary:"):].strip()


# Extract description from the list without brackets
    description = '\n'.join(news_entry.description)

    current_date = datetime.now().strftime("%Y-%m-%d")
# Create a dictionary containing article details
    article_details = {
        'feed_id': current_feed_id,
        'article_id': current_article_id,
        'Link': news_entry.ex_link,
        'title': news_entry.title,
        'details_news':news_entry.details_news,
        'Short description':description,
        'article': {
            "title": title,
            "Summary": summary
        },
        'date': current_date
    }
    if article_text:
        # Article was created
        created_articles.append(article_details)
    else:
        # Article was not created
        not_created_articles.append(news_entry.ex_link)  # Store the link instead
    return current_article_id, article_details

def generate_article_details_chunked(news_entries):
    # Convert each news entry object to a dictionary
    news_dicts = [news_entry.__dict__ for news_entry in news_entries]

    # Set the chunk size to 1 (process one news entry at a time)
    chunk_size = 1

    # Initialize an empty dictionary to store generated articles
    articles_dict = {}

    # Counter for controlling the number of processed chunks
    count = 1

    # Iterate through chunks of news_dicts
    for i in range(0, len(news_dicts), chunk_size):
        print(i)

        # Break the loop if the specified count is reached
        
        # if count > 5:
        #     break
        # else:
        #     count += 1

        # Extract a chunk of news_dicts
        chunk = news_dicts[i:i + chunk_size]

        # Counter for tracking the number of processed news entries within the chunk
        tem_count = 0

        # Iterate through each news_dict in the chunk
        for news_dict in chunk:
            # Generate article details for the current news entry
            article_id, article_details = generate_article_details(
                NewsFeed(
                    feed_id=news_dict['feed_id'],
                    title=news_dict['title'],
                    ex_link=news_dict['ex_link'],
                    details_news=news_dict['details_news'],
                    description=news_dict['description']
                ),
            )

            # Add the generated article details to the articles_dict
            articles_dict[article_id] = article_details
            tem_count += 1

    # Return the final dictionary containing generated articles
    return articles_dict


def get_articles_list():
     # Get the list of news details from the website
    news_details_list = get_news_details_list()
    # Extract relevant information from the news details list and create a list of NewsFeed objects
    news_entries = [NewsFeed(
        feed_id=details_feed.get('feed_id', 0),
        title=details_feed.get('title', ''),
        ex_link=details_feed.get('link', ''),
        details_news=details_feed.get('content', ''),
        description=details_feed.get('description', '')
    ) for details_feed in news_details_list.get('details_list', []) if isinstance(details_feed, dict)]

    total_links = len(news_entries)
    print(f"Total Links: {total_links}")


    generated_articles_dict = generate_article_details_chunked(news_entries)
   # print(f"articles_dict {generated_articles_dict}")

          # Save generated_articles_dict to a text file
    
    # file_name = "articles.txt"
    # with open(file_name, 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(generated_articles_dict, ensure_ascii=False, indent=2))

       # Save links for which articles were not created to a separate file
    
    # not_created_file_name = "not_created_articles.txt"
    # with open(not_created_file_name, 'w', encoding='utf-8') as not_created_file:
    #     not_created_file.write(json.dumps(not_created_articles, ensure_ascii=False, indent=2))

    # print("Articles list saved to:", file_name)
    # print("Not created articles list saved to:", not_created_file_name)

    return generated_articles_dict

   # Call the function to generate articles and save to a text file
#articles_list = get_articles_list()
