import json
import os
from langchain.callbacks.manager import get_openai_callback
from langchain.chat_models.azure_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
#from Details_News import get_news_details_list
from Open_AI_Article_Create_Chat_API import get_articles_list
from QuestionList import GetquestionnaireList

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    with get_openai_callback():
        return model(messages)

def analysis_and_recommendation():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]

    personal_information = {
        "name": "adnan",
        "age": 29,
        "religion": "muslim",
        "education": "graduate from CUET in 2017",
        "family-member": 4,
        "home-town": "Dhaka-Bangladesh",
        "occupation": "software engineer",
        "company": "private ltd",
        "designation": "senior software engineer"
    }

    def extract_article_id_and_content():
    # Obtain a list of articles using the get_articles_list function
        article_info = get_articles_list()

    # Extract relevant information (Feed_id and article) from each article in the list
        extracted_info = [{"Feed_id": article["feed_id"], "article": article["article"]} for article in article_info]

    # Return the extracted information
        return extracted_info


    details_feed = extract_article_id_and_content()
    personal_interest = GetquestionnaireList()
    # personal_interest = {
    #     "trip": {
    #         "What is the primary purpose of your trip?": {"Leisure/Vacation", "Visiting Family or Friends"},
    #         "What type of accommodation do you prefer?": {"Hotel", "Vacation Rental"},
    #         "Which of the following travel apps do you plan to use?": {"Navigation (e.g., Google Maps)"},
    #         "How do you intend to manage your finances while traveling?": {"Using credit/debit cards"},
    #     },
    #     "sports": {
    #         "Who developed Othello, and when was it released under this name?": {"Goro Hasegawa", "Tsukuda in 1973"},
    #         "What was the Japanese name for Reversi during the Meiji period, and who commercialized it?": {"Genpei Go", "Hanayama"},
    #         "When did Hasegawa file a utility model patent related to Othello, and for what purpose?": {"in 1971", "improvement of Genpei Go,"},
    #         "what type of sports do you like most?": {"Indoor", "Outdoor"},
    #         "what sports do you prefer to play?": {"Othello", "cricket", "table-tennis", "volley-ball"},
    #         "What discrepancy or inaccuracy did the author observe in the online articles about Othello?": {"online articles", "Othello is a game that originated in Japan."},
    #         "How does the mention of Othello being a game originated in Japan and Mito City contribute to the author's confusion?": {"Historical Inaccuracy", "Contradiction with Known Facts"}
    #     }
    # }

    request_messages.extend([
        HumanMessage(content=f"""
        Consider yourself as a human nature analyzer. Now analyze this user interest and make a list of his human nature:
        User personal information: {personal_information}
        User interests: {personal_interest}
        """)
    ])
    content_from_api = __call_chat_api(request_messages).content

   # Request to analyze user interest using Chat API
    request_messages.extend([
        HumanMessage(content=f"""
        Consider yourself as a human nature analyzer. Now analyze this user interest and make a list of his human nature:
        User personal information: {personal_information}
        User interests: {personal_interest}
        """)
    ])
    content_from_api = __call_chat_api(request_messages).content

    # Further requests to categorize and match articles
    request_messages.extend([
        AIMessage(content=f"""
                  {content_from_api}
                  """),
        HumanMessage(content=f"""
                     Match this below paragraph list according to the above user interest and categorize this list to best match, average match, and no match. Return JSON format where the key will be match status and the value will be feed ids:
                     {details_feed}
                     Also exclude the paragraph which is not directly related to user interest and return only the id of the list.
                     """)
    ])
    response = __call_chat_api(request_messages).content

    print(response)

# Execute the analysis and recommendation
analysis_and_recommendation()