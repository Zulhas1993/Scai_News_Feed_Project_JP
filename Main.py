from component.OpenAI_Create_Questionnaire import analysis_and_recommendation
from component.Scrapping_Feeds import get_all_links
from component.Open_AI_Article_Create_Chat_API import get_articles_list
from component.User_Article_Json import get_User_articles

# Call the function and print the result
#modified_response = analysis_and_recommendation()
#print(modified_response)
#links= get_all_links()
#print(links)
allArticles = get_articles_list()
userArticles=get_User_articles(allArticles)
print(userArticles)