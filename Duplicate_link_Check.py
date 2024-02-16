from component.Details_News import get_news_details_list

def find_duplicate_links(link_list):
    link_counts = {}
    duplicate_links = set()

    for entry in link_list:
        link = entry.get('Link', '')
        if link in link_counts:
            link_counts[link] += 1
            duplicate_links.add(link)
        else:
            link_counts[link] = 1

    return link_counts

link_lists = get_news_details_list()

duplicate_link_counts = find_duplicate_links(link_lists)

output_file_path = "duplicate_links.txt"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    if duplicate_link_counts:
        output_file.write("Duplicate Links found:\n")
        for link, count in duplicate_link_counts.items():
            output_file.write(f"Link: {link}, Count: {count}\n")
    else:
        output_file.write("No Duplicate Links found.\n")

print(f"Results saved to {output_file_path}")




# def find_unique_links(link_list):
#     unique_links = set()

#     for entry in link_list:
#         link = entry.get('Link', '')
#         unique_links.add(link)

#     return unique_links

# link_lists = get_news_details_list()

# unique_links_set = find_unique_links(link_lists)

# output_file_path = "unique_links.txt"
# with open(output_file_path, "w", encoding="utf-8") as output_file:
#     if unique_links_set:
#         output_file.write("Unique Links found:\n")
#         for link in unique_links_set:
#             output_file.write(f"{link}\n")
#     else:
#         output_file.write("No Unique Links found.\n")

# print(f"Results saved to {output_file_path}")
