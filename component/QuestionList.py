import os
import json
from langchain.callbacks.manager import get_openai_callback
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    with get_openai_callback():
        return model(messages)

def GetquestionnaireList():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]

    personal_information = "I am adnan. I am 29 years old. I am Muslim. I have completed my graduation from CUET in 2017. I have 4 members in my family. I live in Dhaka, Bangladesh. I am working for a private software company as a Senior Software Engineer."

    personal_interest = """
        ("Fascinated by the intricate history and evolution of games, I am drawn to narratives that uncover the origins and cultural nuances behind seemingly simple pastimes. The exploration of Othello's historical ties to Reversi captivates me, revealing a complex interplay of cultural influences, commercial motives, and the dynamic evolution of gaming traditions.",
        "This essay sparks my curiosity about the intersection of creativity, national identity, and commercialization in the world of board games. It inspires me to delve deeper into unique stories that challenge conventional narratives, prompting a thoughtful reflection on the multifaceted aspects of innovation and cultural representation within the gaming industry.")
    """

    details_feed = """
        ("The essay discusses the historical origins of the game Othello and its connection to the game Reversi. Despite claims that Othello is a Japanese game originating in Mito City, the author clarifies that it was developed by Goro Hasegawa and released by Tsukuda in 1973, drawing its name from Shakespeare's play.",
        "The essay highlights that Reversi, a similar game, existed in England in the 1890s and was known as "Genpei Go" when introduced to Japan during the Meiji period. The commercialization of Reversi preceded Othello, and Hasegawa filed a patent in 1971, categorizing it as an improvement. ",
        "The narrative explores Hasegawa's shift in attributing Othello to his invention called Pincer Go around 2000. The author criticizes Hasegawa and Megahouse for asserting Othello's uniqueness for brand value and financial gain. In essence, the essay challenges the narrative of Othello as a purely Japanese creation, emphasizing its historical ties to Reversi and underscoring the commercial motives behind asserting its distinctiveness.")
    """

    request_messages.extend([
        HumanMessage(content=f"If you are looking for information about Othello, please list 20 things you need")
    ])

    # Make the API call
    response = __call_chat_api(request_messages)

    # Convert content_from_api to string
    content_from_api = response.content if isinstance(response, AIMessage) else str(response)
    content_str = str(content_from_api)

    request_messages.extend([
        AIMessage(content=f"{content_str}"),
        HumanMessage(content="make a questionnaire based on the above things with 4 options as json format where key will be question and value will be options and remove from start side ```json and remove from end side ``` ")
    ])

    # Make another API call with updated messages
    response = __call_chat_api(request_messages).content
    response_content = response.content if isinstance(response, AIMessage) else str(response)

    # Parse the response content to extract questions and options
    questions_and_options = json.loads(response_content)

    # Create a dictionary to hold the final response
    final_response = {}

    # Assign options directly to final_response[question]
    for question, options in questions_and_options.items():
        final_response[question] = options

     # Create a dictionary for options
        # option_dict = {opt: None for opt in options}
        # final_response[question] = option_dict

    # Convert the dictionary to JSON format
    response_json = json.dumps(final_response, ensure_ascii=False, indent=2)
    #print(response_json)
    return response_json

GetquestionnaireList()
