import sys
sys.path.append(r'E:\Final_Project_for_Git\Scai_News_Feed_Project_JP\component')

from component.Scrapping_Feeds import get_all_links
from component.Details_News import extract_news_info
# from Open_AI_Article_Create_Chat_API import get_news_details_list, get_articles_list
# from Article_list import get_articles_list

scrapping_data = get_all_links()
#print(scrapping_data)
extract_news_info_from_scrapping_data = extract_news_info(scrapping_data)
print(extract_news_info_from_scrapping_data)

# news_details_list = get_news_details_list()
# print(news_details_list)

# article_list = get_articles_list()
# print(article_list)

# print(extract_news_info_from_scrapping_data)
