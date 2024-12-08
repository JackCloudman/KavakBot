import json
import os
import time
from typing import Any, Dict, List

import pandas as pd
import requests

# Wait to ensure that Typesense is up and running
time.sleep(5)

# Typesense configuration from environment variables or default values
TYPESENSE_HOST: str = os.getenv("TYPESENSE_HOST", "typesense")
TYPESENSE_PORT: str = os.getenv("TYPESENSE_PORT", "8108")
API_KEY: str = os.getenv("TYPESENSE_API_KEY", "abcd1234")

base_url: str = f"http://{TYPESENSE_HOST}:{TYPESENSE_PORT}"

# Read the cleaned CSV
df: pd.DataFrame = pd.read_csv("data/cars_cleaned_enriched.csv")

# Assuming the CSV is clean, we still fill any potential missing values
# Define columns based on updated names
str_cols: List[str] = ['make', 'model', 'version', 'description']
bool_cols: List[str] = ['bluetooth', 'carplay']
num_cols: List[str] = ['stock_id', 'kilometers',
                       'price', 'year', 'length', 'width', 'height']

# Fill missing values in string columns
for col in str_cols:
    df[col] = df[col].fillna("")

# Fill missing values in numeric columns
for col in num_cols:
    df[col] = df[col].fillna(0)

# Fill missing values in boolean columns
for col in bool_cols:
    df[col] = df[col].fillna(False)

# Convert data types appropriately
df['stock_id'] = df['stock_id'].astype(int)
df['kilometers'] = df['kilometers'].astype(int)
df['year'] = df['year'].astype(int)
df['price'] = df['price'].astype(float)
df['length'] = df['length'].astype(float)
df['width'] = df['width'].astype(float)
df['height'] = df['height'].astype(float)
df['bluetooth'] = df['bluetooth'].astype(bool)
df['carplay'] = df['carplay'].astype(bool)

# Define the schema for the Typesense collection
collection_name: str = "cars"
collection_schema: Dict[str, Any] = {
    "name": collection_name,
    "fields": [
        {"name": "stock_id", "type": "int32"},
        {"name": "kilometers", "type": "int32"},
        {"name": "price", "type": "float"},
        {"name": "make", "type": "string"},
        {"name": "model", "type": "string"},
        {"name": "year", "type": "int32"},
        {"name": "version", "type": "string"},
        {"name": "bluetooth", "type": "bool"},
        {"name": "length", "type": "float"},
        {"name": "width", "type": "float"},
        {"name": "height", "type": "float"},
        {"name": "carplay", "type": "bool"},
        {"name": "description", "type": "string"}
    ],
    "default_sorting_field": "price"  # Optional: set a default sorting field
}

# Delete the collection if it already exists to avoid schema conflicts
delete_response = requests.delete(
    f"{base_url}/collections/{collection_name}",
    headers={"X-TYPESENSE-API-KEY": API_KEY}
)

if delete_response.status_code in [200, 404]:
    print(
        f"Collection '{collection_name}' deleted or did not exist previously.")
else:
    print(f"Error deleting the collection: {delete_response.text}")

# Create the collection
create_response: requests.Response = requests.post(
    f"{base_url}/collections",
    headers={"X-TYPESENSE-API-KEY": API_KEY},
    json=collection_schema
)

if create_response.status_code == 201:
    print("Collection created successfully.")
else:
    print(f"Error creating the collection: {create_response.text}")

# Convert the DataFrame to a list of dictionaries
documents: List[Dict[str, Any]] = df.to_dict(orient="records")

# Bulk import documents
# Typesense expects one JSON document per line
bulk_data: str = "\n".join([json.dumps(doc) for doc in documents])

import_response = requests.post(
    f"{base_url}/collections/{collection_name}/documents/import",
    headers={
        "X-TYPESENSE-API-KEY": API_KEY,
        "Content-Type": "text/plain"
    },
    data=bulk_data
)

if import_response.status_code == 200:
    print("Documents inserted successfully.")
else:
    print(f"Error inserting documents: {import_response.text}")
