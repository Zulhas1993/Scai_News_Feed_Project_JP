from azure.storage.blob import BlobServiceClient
from io import BytesIO
import pandas as pd

# SQL query
query = 'SELECT * FROM users'

# Execute the query and fetch data into a DataFrame
df = pd.read_sql(query, conn)

# Azure Storage connection string and container name
connection_string = '<your_storage_account_connection_string>'
container_name = '<your_blob_container_name>'

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

# Convert DataFrame to CSV in memory
csv_data = df.to_csv(index=False)
csv_bytes = BytesIO(csv_data.encode())

# Upload CSV to Blob Storage
blob_name = 'users_data.csv'
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(csv_bytes)
