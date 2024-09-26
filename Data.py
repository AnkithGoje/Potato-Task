import pandas as pd
from pymongo import MongoClient

def ingest_tsv_to_mongo(tsv_file_path):
    # Step 1: Read the TSV file
    data = pd.read_csv(tsv_file_path, sep='\t')
    
    # Step 2: Clean and transform data
    data['ts1'] = pd.to_datetime(data['ts1'])  # Convert timestamp to datetime
    data[' ts2'] = pd.to_datetime(data[' ts2'])  # Fix the leading space in ' ts2' column name
    data['created_at'] = pd.to_datetime(data['created_at'], utc=True)
    
    # Step 3: Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.twitter_db
    collection = db.tweets
    
    # Step 4: Check if data already exists to avoid duplicate ingestion
    if collection.count_documents({}) > 0:
        print("Data already exists in MongoDB, skipping ingestion.")
        return
    
    # Step 5: Insert data into MongoDB
    collection.insert_many(data.to_dict(orient='records'))
    
    print("Data ingested successfully into MongoDB!")
