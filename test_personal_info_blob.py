from azure.storage.blob import BlobServiceClient
import json

# Replace these with your actual Azure Storage account and blob information
account_name = "your_storage_account_name"
account_key = "your_storage_account_key"
container_name = "your_container_name"
blob_name = "your_blob_name.json"

# Create a BlobServiceClient
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# Get a reference to the blob
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)


# Download the blob content
blob_content = blob_client.download_blob()
json_data = blob_content.readall()

# Decode the JSON data
personal_information = json.loads(json_data)

# Print or use the extracted information
print(personal_information)
