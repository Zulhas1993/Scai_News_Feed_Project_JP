import json
import requests
from bs4 import BeautifulSoup
from docx import Document

class FetchDetailsError(Exception):
    pass

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

def get_news_details(link):
    try:
        # You can customize this function to fetch news details from the provided link
        response = requests.get(link)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the webpage
        details_text = soup.get_text()

        # Check if the details_text is not empty or contains only whitespace
        if details_text and not details_text.isspace():
            # Return the news details
            return {'content': details_text}
        else:
            # Return None if there are no details
            return None
    except requests.RequestException as e:
        raise FetchDetailsError(f"Error fetching details for link: {link}. {str(e)}")

def extract_news_info(data):
    news_list = []
    unique_links = set()  # Use a set to track unique links

    for key, value in data.items():
        for entry in value.values():
            entry_data = json.loads(entry)
            title = entry_data.get('title', '')
            link = entry_data.get('link', '')
            description = entry_data.get('description', '')
            subjectList = entry_data.get('subjectList', [])

            # Check if the link is not a duplicate and has details
            if link not in unique_links and description:
                news_list.append({'title': title, 'link': link, 'description': description, 'subjectList': subjectList})
                unique_links.add(link)

    return news_list

def generate_news_details_list():
    try:
        file_path = 'object_list.json'

        # Read JSON file
        data = read_json(file_path)

        # Extract news information
        news_list = extract_news_info(data)
        details_list = []

        for news in news_list:
            link = news.get('link', '')
            try:
                # Fetch details for each link
                news_details = get_news_details(link)

                if news_details:
                    # Append details to the list
                    details_list.append({
                        "title": news.get('title', ''),
                        "link": link,
                        "details": news_details
                    })
            except FetchDetailsError as e:
                print(f"An error occurred while fetching details for link: {link}. {str(e)}")

        return details_list

    except Exception as e:
        print(f"An error occurred during news details generation: {e}")
        return None

def save_to_docx(news_details_list):
    try:
        doc = Document()

        for news_details in news_details_list:
            title = news_details.get('title', '')
            link = news_details.get('link', '')
            details = news_details.get('details', {}).get('content', '')

            doc.add_heading(title, level=1)
            doc.add_paragraph(f"Link: {link}")
            doc.add_paragraph(details)
            doc.add_page_break()

        doc.save('news_details.docx')
        print("News details saved to news_details.docx")

    except Exception as e:
        print(f"An error occurred while saving to DOCX: {e}")

# Generate news details list
generated_details_list = generate_news_details_list()

# Save to DOCX
if generated_details_list:
    save_to_docx(generated_details_list)
