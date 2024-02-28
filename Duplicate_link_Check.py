import json
from component.Details_News import get_news_details_list
from component.Scrapping_Feeds import get_all_links

# Function to read JSON data from a file
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            data = json.load(file)
            print(f"Data loaded from {file_path}: {data}")
        return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

# Get new scraping links
new_scraping_links = get_all_links()

# Read previous data from the file
file_path = 'object_list.json'
previous_data = read_json(file_path)

def filter_duplicate_links(new_links, existing_data):
    existing_links = {entry.get('Link', '') for entry in existing_data}

    # Filter out duplicate links from new scraping data
    filtered_new_links = [entry for entry in new_links if entry.get('Link', '') not in existing_links]

    return filtered_new_links

filtered_new_data = filter_duplicate_links(new_scraping_links, previous_data)

# Write the filtered new data to a file
output_file_path = "filtered_new_data.json"
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(filtered_new_data, output_file, ensure_ascii=False, indent=2)

print(f"Filtered new data saved to {output_file_path}")
