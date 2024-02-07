from datetime import datetime
import json
from Models.Tag import Tags



class Tags:
    def __init__(self, id, tag_name, created_at, deleted_at, updated_at):
        self.id = id
        self.tag_name = tag_name
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.updated_at = updated_at

def add_tags(item_id, tag_name):
    """
    Add new tags to an item identified by item_id.

    :param item_id: Identifier for the item.
    :param tag_name: String containing the tag name.
    :return: Success message or error message.
    """
    try:
        # Assuming you have a function to retrieve the existing tags for the item from the data store
        existing_tags = get_existing_tags(item_id)

        # Combine existing tags with the new tag (ensuring no duplicates)
        updated_tags = list(set(existing_tags + [tag_name.strip()]))

        # Assuming you have a function to update the tags in the data store
        update_tags_in_data_store(item_id, updated_tags)

        return "Tag added successfully."
    except Exception as e:
        return f"Error adding tag: {str(e)}"

# Create an instance of the Tags class
tag_instance = Tags(id=123, tag_name="example_tag", created_at="", deleted_at="", updated_at="")
# Call the add_tags function with the instance
result_message = add_tags(tag_instance.id, tag_instance.tag_name)
print(result_message)


current_date = datetime.now().strftime("%Y-%m-%d")
tag_store = {}
def create_tag(tag_name):
    tag_id = len(tag_store) + 1
    created_at = current_date
    tag = Tags(id=tag_id, tag_name=tag_name, created_at=created_at, deleted_at=current_date, updated_at=current_date)
    tag_store[tag_id] = tag
    return tag



def update_tags(tag_id, updated_tags):
    """
    Update tags for an item identified by tag_id.

    :param tag_id: Identifier for the tag.
    :param updated_tags: String containing tags separated by commas.
    :return: Success message or error message.
    """
    try:
        # Split the updated_tags into a list of tags
        tags_list = [tag.strip() for tag in updated_tags.split(',')]

        # Assuming you have a function to update the tags in the data store
        update_tags_in_data_store(tag_id, tags_list)

        return "Tags updated successfully."
    except Exception as e:
        return f"Error updating tags: {str(e)}"



def Get_tag_by_Id(tag_id):
    return tag_store.get(tag_id)

def update_tag(tag_id, new_tag_name):
    tag = tag_store.get(tag_id)
    if tag:
        tag.tag_name = new_tag_name
        tag.updated_at = current_date  # Replace with the actual timestamp
        return tag
    return None



def delete_tags(tag_id, tags_to_delete):
    """
    Delete specific tags from an item identified by item_id.

    :param item_id: Identifier for the item.
    :param tags_to_delete: List of tags to be deleted.
    :return: Success message or error message.
    """
    try:
        # Assuming you have a function to retrieve the existing tags for the item from the data store
        existing_tags = get_existing_tags(tag_id)

        # Remove specified tags
        updated_tags = [tag for tag in existing_tags if tag not in tags_to_delete]

        # Assuming you have a function to update the tags in the data store
        update_tags_in_data_store(tag_id, updated_tags)

        return "Tags deleted successfully."
    except Exception as e:
        return f"Error deleting tags: {str(e)}"


def delete_tag(tag_id):
    tag = tag_store.pop(tag_id, None) # pop deleted tag
    if tag:
        tag.deleted_at = current_date  # Replace with the actual timestamp
    return tag

def list_all_tags():






    
    return list(tag_store.values())


def user_wise_tags_list(user_id):
    user_tags = [tag for tag in tag_store.values() if tag.user_id == user_id]
    return user_tags

# Assuming you have a global dictionary as a simple data store
data_store = {
    1: ["python", "programming", "tutorial"],
    2: ["web", "development", "javascript"],

}

def get_existing_tags(tag_id):
    """
    Retrieve existing tags for an item identified by tag_id.
    :param tag_id: Identifier for the item.
    :return: List of existing tags for the item.
    """
    # Assuming item_id exists in the data store
    if tag_id in data_store:
        return data_store[tag_id]
    else:
        # Return an empty list if item_id not found
        return []

def update_tags_in_data_store(tag_id, new_tags):
    """
    Update tags for an item identified by tag_id in the data store.

    :param tag_id: Identifier for the item.
    :param new_tags: List of new tags to be set for the item.
    :return: True if update is successful, False otherwise.
    """
    # Check if item_id exists in the data store
    if tag_id in data_store:
        # Update the tags for the item
        data_store[tag_id] = new_tags
        return True
    else:
        # Return False if item_id not found
        return False
    

#*************************Using blob storage *************************

def add_tag(tag):
    # Convert the tag object to JSON
    tag_json = json.dumps(tag.__dict__)
    # Create a blob client
    blob_client = container_client.get_blob_client(f"{tag.id}.json")
    # Upload the tag JSON to the blob
    blob_client.upload_blob(tag_json, content_settings=ContentSettings(content_type='application/json'))


def list_tags():
    tags = []

    # List all blobs in the container
    blob_list = container_client.get_blobs()
    for blob in blob_list:
        # Download the blob content
        blob_client = container_client.get_blob_client(blob.name)
        content = blob_client.download_blob().readall()

        # Parse the JSON content and create a Tag object
        tag_dict = json.loads(content)
        tag = Tags(**tag_dict)
        tags.append(tag)

    return tags        

def update_tag(tag_id, updated_tag):
    # Convert the updated tag object to JSON
    updated_tag_json = json.dumps(updated_tag.__dict__)

    # Create a blob client
    blob_client = container_client.get_blob_client(f"{tag_id}.json")

    # Upload the updated tag JSON to the blob
    blob_client.upload_blob(updated_tag_json, content_settings=ContentSettings(content_type='application/json'))

def delete_tag(tag_id):
    # Create a blob client
    blob_client = container_client.get_blob_client(f"{tag_id}.json")

    # Delete the blob
    blob_client.delete_blob()


def get_tag_by_id(tag_id):
    try:
        # Create a blob client
        blob_client = container_client.get_blob_client(f"{tag_id}.json")

        # Download the blob content
        content = blob_client.download_blob().readall()

        # Parse the JSON content and create a Tag object
        tag_dict = json.loads(content)
        tag = Tags(**tag_dict)

        return tag
    except Exception as e:
        print(f"Error retrieving tag with ID {tag_id}: {str(e)}")
        return None
