import json
from datetime import datetime
from Open_AI_Article_Create_Chat_API import get_articles_list

class UserArticle:
    def __init__(self, id, themeId, title, ex_link, article, date, created_at, updated_at, deleted_at):
        self.id = id
        self.themeId = themeId
        self.title = title
        self.ex_link = ex_link
        self.article = article
        self.date = date
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

def get_User_articles(articles_list):
    # Initialize an empty dictionary to store the formatted articles
    formatted_json = {}

    # Get the current date in the format 'YYYY-MM-DD'
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Assign a default themeId (you may modify this according to your theme logic)
    themeId = 1

    # Iterate through each article in the provided articles_list
    for article in articles_list:
        # Retrieve relevant information from the article
        article_id = article.get('article_id', '')
        title = article.get('title', '')
        link = article.get('Link', '')  # Use 'Link' key
        article_content = article.get('article', '')
        article_date = article.get('date', '')

        # Update the formatted_json dictionary with the article information
        formatted_json.setdefault(current_date, {}).setdefault(article_id, {}).update({
            'themeId': themeId,
            'title': title,
            'link': link,
            'article': article_content,
            'date': article_date
        })

    # Return the formatted dictionary
    return formatted_json



# Assuming get_articles_list() returns a list of UserArticle instances
allArticles = get_articles_list()

# Use the format_articles_to_json function to get the desired JSON format
formatted_json_result = get_User_articles(allArticles)

# Return the formatted JSON result
#print (json.dumps(formatted_json_result, ensure_ascii=False, indent=2))
