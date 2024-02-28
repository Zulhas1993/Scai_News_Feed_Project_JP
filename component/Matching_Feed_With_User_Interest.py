import json
import os
from langchain.callbacks.manager import get_openai_callback
from langchain.chat_models.azure_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from Article_list import get_articles_list
from QuestionList import GetquestionnaireList
from Details_News import read_json

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    with get_openai_callback():
        return model(messages)

def extract_key_and_content():
    # Get the article information using the get_articles_list function
    article_info = get_articles_list()

    # Initialize an empty dictionary to store the extracted information
    extracted_info = {}

    # Iterate over each key-value pair in the article_info dictionary
    for key, article in article_info.items():
        # Extract relevant information (Link, title, and summary) for each article
        extracted_info[key] = {
            "Link": article["Link"],
            "title": article["title"],
            "summary": article["article"]["Summary"]
        }

    # Return the dictionary containing the extracted information for each article
    return extracted_info


def Match_Feed_Or_Article_With_User_Interest():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]
    # file_path = 'object_list.json'
    # data = read_json(file_path)

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

    details_feed = extract_key_and_content()
    personal_interest = GetquestionnaireList()

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
        AIMessage(content=f"{content_from_api}"),
        HumanMessage(content=f"""
                     Match this below paragraph list according to the above user interest and categorize this list to best match, average match, and no match. If best_match is empty, then find any keyword that matches with the {details_feed} then it considers the best match. Return JSON format where the key will be match status and the value will be feed ids and JSON format will be {{"Match_Status":{{"best_match":[],"average_match":[],"no_match":[]}}}} :
                     {details_feed}
                     Also exclude the paragraph which is not directly related to user interest and return only the id of the list.
                     """)
    ])
    response = __call_chat_api(request_messages).content

    # Print the response to a text file
    output_file_path = "matchStatus.txt"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(response, ensure_ascii=False, indent=2))

    print(f"Response saved to {output_file_path}")
    return response

# Execute the analysis and recommendation
Match_Feed_Or_Article_With_User_Interest()
