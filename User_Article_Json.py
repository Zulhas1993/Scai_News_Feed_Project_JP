import json
from datetime import datetime
from Article_Create_Using_Chat_AI import get_articles_list

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
    formatted_json = {}
    current_date = datetime.now().strftime("%Y-%m-%d")
    themeId = 1
    for article in articles_list:
        article_id = article.get('article_id', '')
        formatted_json.setdefault(current_date, {}).setdefault(article_id, {}).update({
            'themeId': themeId,
            'title': article.get('title', ''),
            'link': article.get('Link', ''),  # Update to use 'Link'
            'article': article.get('article', ''),
            'date': article.get('date', '')
        })

    return formatted_json


# Assuming get_articles_list() returns a list of UserArticle instances
allArticles = get_articles_list()

# Use the format_articles_to_json function to get the desired JSON format
formatted_json_result = get_User_articles(allArticles)

# Return the formatted JSON result
print (json.dumps(formatted_json_result, ensure_ascii=False, indent=2))
