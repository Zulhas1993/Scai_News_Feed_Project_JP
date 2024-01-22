import json
import requests
from bs4 import BeautifulSoup
from docx import Document  

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        data = json.load(file)
    return data

def extract_news_info(data):
    news_list = []
    for key, value in data.items():
        for entry in value.values():
            entry_data = json.loads(entry)
            title = entry_data.get('title', '')
            link = entry_data.get('link', '')
            description = entry_data.get('description', '')
            tags = entry_data.get('subjectList', [])
            news_list.append({'title': title, 'link': link, 'description': description, 'tags': tags})
    return news_list

def get_news_details(link):
    # You can customize this function to fetch news details from the provided link
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content from the webpage
        details_text = soup.get_text()
        
        print(details_text)
        # Truncate or summarize the content if it's too large
        max_document_size = 5120  # Maximum allowed text elements
        if len(details_text) > max_document_size:
            details_text = details_text[:max_document_size]
            
        # Return the news details
        return {'content': details_text}
    else:
        print(f"Error fetching details for link: {link}")
        return None
    
class FetchDetailsError(Exception):
    pass

def save_news_details_to_doc(news_list, output_file='news_details.doc'):
    with open(output_file, 'w', encoding='utf-8') as file:
        for news in news_list:
            file.write(f"Title: {news['title']}\n")
            file.write(f"Link: {news['link']}\n")
            file.write(f"Description: {news['description']}\n")
            file.write(f"Subjects: {', '.join(news['subjectList'])}\n")
            
            # Check if 'content' key is present before accessing it
            content = news.get('content', '')
            file.write(f"Content: {content}\n\n")


def get_ex_links(news_list):
    links = []

    for news in news_list:
        link = news['link']
        links.append(link)
        print(links)
    return links
SystemExit

if __name__ == "__main__":
    file_path = 'object_list.json'
    
    # Read JSON file
    data = read_json(file_path)
    
    # Extract news information
    news_list = extract_news_info(data)

    # Fetch news details for each link
    for news in news_list:
        link = news['link']
        try:
            news_details = get_news_details(link)
            if news_details:
                # Add the fetched details to the news dictionary
                news.update(news_details)
        except FetchDetailsError as e:
            print(str(e))  # Handle or log the error as needed

    # Save news details to a Word document
    save_news_details_to_doc(news_list, output_file='news_details.docx')
    
    # Save links with details to a Word document
    get_ex_links(news_list, output_file='links.docx')
    
    print("News details saved to 'news_details.docx'")
    print("Links with details saved to 'links.docx'")
