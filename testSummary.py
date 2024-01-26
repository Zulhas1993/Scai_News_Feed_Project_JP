import json
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
    key = "09b7c88cfff44bac95c83a2256f31907"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def generate_abstractive_summary(text_analytics_client, document):
    poller = text_analytics_client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            print("Summaries abstracted:")
            [print(f"{summary.text}\n") for summary in result.summaries]
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))

if __name__ == "__main__":
    # Authenticate the Text Analytics client
    text_analytics_client = authenticate_client()

    # Define your documents
    document = [
        "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, "
        "human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI Cognitive "
        "Services, I have been working with a team of amazing scientists and engineers to turn this quest into a "
        "reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of "
        "human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the "
        "intersection of all three, there's magic-what we call XYZ-code as illustrated in Figure 1-a joint "
        "representation to create more powerful AI that can speak, hear, see, and understand humans better. "
        "We believe XYZ-code will enable us to fulfill our long-term vision: cross-domain transfer learning, "
        "spanning modalities and languages. The goal is to have pretrained models that can jointly learn "
        "representations to support a broad range of downstream AI tasks, much in the way humans do today. "
        "Over the past five years, we have achieved human performance on benchmarks in conversational speech "
        "recognition, machine translation, conversational question answering, machine reading comprehension, "
        "and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious "
        "aspiration to produce a leap in AI capabilities, achieving multisensory and multilingual learning that "
        "is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational "
        "component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
    ]


    # Initialize a dictionary to store the summaries
    all_summaries_dict = {}

    # Generate abstractive summaries for each document
    for idx, document in enumerate(document, start=1):
        summaries = generate_abstractive_summary(text_analytics_client, document)
        all_summaries_dict[f"Document_{idx}"] = {
            'text': document,
            'summaries': summaries
        }

    # Write the dictionary to a JSON file
    output_file_path = 'summaries_output.json'
    with open(output_file_path, 'w', encoding='utf-16') as json_file:
        json.dump(all_summaries_dict, json_file, ensure_ascii=False, indent=4)

    print(f"Summaries have been written to {output_file_path}")
