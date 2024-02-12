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

def GetquestionnaireList(tag="Othello"):
    request_messages = [
        SystemMessage(content="Please answer in English"),
        HumanMessage(content=f"If you are looking for information about {tag}, please list 20 things you need")
    ]

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
    final_response = {tag: {}}

    # Assign options directly to final_response[tag][question]
    for question, options in questions_and_options.items():
        final_response[tag][question] = options

    # Convert the dictionary to JSON format
    response_json = json.dumps(final_response, ensure_ascii=False, indent=2)
    print(response_json)
    return response_json

# Call the function and print the result
GetquestionnaireList()
