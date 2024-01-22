import os
from langchain.callbacks.manager import get_openai_callback
from langchain.chat_models.azure_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
#from langchain_openai import AzureChatOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    with get_openai_callback():
        return model(messages)

def format_questionnaire_json(questionnaire_content: str) -> dict:
    if isinstance(questionnaire_content, str):
        questions_and_options = [line.strip() for line in questionnaire_content.split('\n\n') if line.strip()]
        formatted_data = {"questions": []}

        for question_and_options in questions_and_options[1:]:
            # Skip the first line as it contains a sample introduction
            question_lines = question_and_options.strip().split('\n', 1)
            if len(question_lines) == 2:
                question_number, question_text = question_lines[0].split('.', 1)
                options = [line.strip()[3:] for line in question_lines[1].split('\n')]
                if options:
                    # Remove prefix ')' from each option
                    options = [opt[2:] for opt in options]
                    formatted_data["questions"].append({
                        "question": question_text.strip(),
                        "options": options
                    })
            else:
                # Handle the case where there is no dot ('.') on the first line
                question_text = question_lines[0]
                formatted_data["questions"].append({
                    "question": question_text.strip(),
                    "options": []
                })
        return formatted_data
    else:
        raise ValueError("Invalid content type. Expected string.")

def analysis_and_recommendation():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]

    personal_information = "I am adnan. I am 29 years old. I am Muslim. I have completed my graduation from CUET in 2017. I have 4 members in my family. I live in Dhaka, Bangladesh. I am working for a private software company as a Senior Software Engineer."

    personal_interest = """
        ("Relaxation and adventure motivate me to travel, adventure and budget traveller, beaches and mountains are my travel destinations, travel agent will plan for my travel, planning for international travel",
        "Artificial Intelligence. Recent news for AI. AI documentations. AI machines. Microsoft AI services")
    """

    details_feed = """
        ("Historic books are portals to bygone eras, preserving the collective wisdom and tales of civilizations past. Through the weathered pages, one glimpses the evolution of ideas, cultures, and societies. These literary treasures bridge the gap between epochs, offering timeless insights that illuminate the rich tapestry of human history.",
        "Mobile phones have evolved from communication tools to indispensable companions. These pocket-sized marvels connect the world, offering instant communication, entertainment, and productivity. With sleek designs and powerful capabilities, they redefine daily life, providing access to information and connecting people across the globe in the palm of our hands.",
        "Web development is the art of crafting digital experiences, seamlessly blending creativity and technology. It encompasses designing and coding websites, ensuring functionality and aesthetic appeal. From front-end interfaces to back-end databases, web developers navigate the ever-evolving landscape of programming languages and frameworks, shaping the online world's dynamic presence.")
    """

    request_messages.extend([
        HumanMessage(content=f"""
        If you are looking for information about a trip, please list 20 things you need
        """
        )
    ])

    # Make the API call
    response = __call_chat_api(request_messages)

    # Convert content_from_api to string
    content_from_api = response.content if isinstance(response, AIMessage) else str(response)
    content_str = str(content_from_api)

    request_messages.extend([
        AIMessage(content=f"{content_str}"),
        HumanMessage(content="""
                     make a questionnaire based on the above things with 4 options
                     """)
    ])

    # Make another API call with updated messages
    response = __call_chat_api(request_messages).content
    #print(response)
    # Ensure response is a string
    response_content = response.content if isinstance(response, AIMessage) else str(response)

    formatted_response = format_questionnaire_json(response_content)
    
    # Remove questions with empty options
    formatted_response["questions"] = [q for q in formatted_response["questions"] if q["options"]]
    
    # Modify the formatted response to match the expected result format
    modified_response = {
        "questions": formatted_response["questions"]
    }
    
    
    print(modified_response)

# Call the main function
analysis_and_recommendation()
