from component.Scrapping_Feeds import get_all_links
from component.Article_list import get_articles_list
from component.News_Feed_Json import News_Feed_Json_Return
from component.Date_wise_news_feed import generate_date_wise_news_feed_list
from component.QuestionList import GetquestionnaireList
from component.Open_AI_Article_Create_Chat_API import get_news_details_list
import json

# from Details_News import (
#     get_all_links,
#     read_json,
#     extract_news_info,
#     get_news_details,
#     get_news_details_list,
#     generate_date_wise_news_feed_list,
#     GetquestionnaireList,
#     get_articles_list,
#     News_Feed_Json_Return,
# )

NewsFeedList = News_Feed_Json_Return()
print(NewsFeedList)

# def run_all_functions():
#     # Function to run all necessary functions and print NewsFeedList

#     # Define the file path
#     # file_path = 'object_list1.json'

#     # # Get all links
#     # links = get_all_links()
    
#     # # Read JSON file
#     # data = read_json(file_path)
    
#     # # Extract news information
#     # extrctnews = extract_news_info(data)
    
#     # # Get news details
#     # detailsNews = get_news_details()
    
#     # # Get news details list
#     # DetailsNewsList = get_news_details_list()
    
#     # # Generate date-wise news feed list
#     # dateWiseFeed = generate_date_wise_news_feed_list()
    
#     # # Get questionnaire list
#     # Questions = GetquestionnaireList()
    
#     # # Get articles list
#     # ArticleList = get_articles_list()
    
#     # Get News Feed List
#     NewsFeedList = News_Feed_Json_Return()

#     # Print NewsFeedList
#     print("NewsFeedList:", json.dumps(NewsFeedList, ensure_ascii=False, indent=2))

# # Run all functions
# run_all_functions()



