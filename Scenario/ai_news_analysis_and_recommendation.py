
from component.Scrapping_Feeds import get_all_links
from component.Details_News import extract_news_info, read_json
from component.Open_AI_Article_Create_Chat_API import get_news_details_list, get_articles_list



def execute_all_functions(file_path='object_list.json'):
    # 1. Get scrapping data
    scrapping_data = get_all_links()

    # 2. Extract news info from scrapping data
    extract_news_info_from_scrapping_data = extract_news_info(read_json(file_path))

    # 3. Get news details list
    news_details_list = get_news_details_list()
    
    # 4. Get Article list
    artcle_list = get_articles_list()

    # Print or return the results as needed
    print("Scrapping Data:")
    print(scrapping_data)

    print("\nExtracted News Info:")
    print(extract_news_info_from_scrapping_data)

    print("\nNews Details List:")
    print(news_details_list)

    print("\nArticle List:")
    print(artcle_list)

    return scrapping_data, extract_news_info_from_scrapping_data, news_details_list, artcle_list

# Dynamically set the file path based on another variable
dynamic_file_path = 'path/to/name/file.json'
result_scrapping, result_extract_info, result_news_details, result_article_list = execute_all_functions(file_path=dynamic_file_path)



