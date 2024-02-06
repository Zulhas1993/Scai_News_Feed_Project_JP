from Models.Tag import Tags



# class Tags:
#     def __init__(self, id, tag_name, created_at, deleted_at, updated_at):
#         self.id = id
#         self.tag_name = tag_name
#         self.created_at = created_at
#         self.deleted_at = deleted_at
#         self.updated_at = updated_at

def add_tags(tags_object):
    """
    Add new tags to an item identified by item_id.

    :param tags_object: Instance of Tags class containing tag information.
    :return: Success message or error message.
    """
    try:
        # Assuming you have a function to retrieve the existing tags for the item from the data store
        existing_tags = get_existing_tags(tags_object.id)

        # Combine existing tags with new tags (ensuring no duplicates)
        updated_tags = list(set(existing_tags + tags_object.tag_name))

        # Assuming you have a function to update the tags in the data store
        update_tags_in_data_store(tags_object.id, updated_tags)

        return "Tags added successfully."
    except Exception as e:
        return f"Error adding tags: {str(e)}"


def update_tags(tag_id, updated_tags):
    """
    Update tags for an item identified by item_id.

    :param item_id: Identifier for the item.
    :param updated_tags: List of updated tags.
    :return: Success message or error message.
    """
    try:
        # Assuming you have a function to update the tags in the data store
        update_tags_in_data_store(tag_id, updated_tags)

        return "Tags updated successfully."
    except Exception as e:
        return f"Error updating tags: {str(e)}"


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