# POTATO Take-Home Task #

This project is a Flask-based web application that ingests data from a TSV file and stores it in a MongoDB collection. It provides an API to query tweets stored in MongoDB based on specific terms. The ingestion and querying processes are handled by two Python scripts: Data.py (for data ingestion) and app.py (for running the Flask API).

## Features
Ingests data from a TSV file into MongoDB.
Provides a REST API to:
Count tweets per day containing a search term.
Calculate the average number of likes.
Group tweets by hour.
Find unique users and top users.
Uses MongoDB to store and query tweet data.

## Install Dependencies
Set up a virtual environment and install dependencies:
```
# Create and activate a virtual environment
python -m venv venv 
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate      # For Windows
```
```
# Install the required packages
pip install -r requirements.txt
```
## Set Up MongoDB
Make sure you have MongoDB running locally or via a cloud instance (e.g., MongoDB Atlas).
  If MongoDB is installed locally, ensure it’s running on ```mongodb://localhost:27017/```.

## Usage
### 1. Ingest Data
Before running the Flask application, you need to ingest the data from the TSV file into MongoDB.
```
# Run ingestion.py to load the data
python ingestion.py
```
This script reads data from the specified TSV file, transforms it, and stores it in MongoDB.


### 2. Run the Flask Application
After the data has been ingested, you can run the Flask application:
```
python app.py
```
The application will be running on http://localhost:5000/.

## API Endpoints
### 1. Query Tweets
**Endpoint:** ```/query_tweets```

**Method:** GET

**Description:** Queries the database for tweets containing a specific term and returns aggregated data.

### Query Parameters:
* ```term``` (required): The search term to look for in the tweet text.

**Example Request:**
```
GET http://localhost:5000/query_tweets?term=python
```
**Example Response:**
```
json
{
  "tweets_per_day": [
    {"_id": "2024-09-26", "count": 150}
  ],
  "unique_users_count": 50,
  "average_likes": [
    {"_id": null, "average_likes": 120}
  ],
  "places": [
    {"_id": "NYC123"}
  ],
  "tweet_times": [
    {"_id": 14, "count": 20}
  ],
  "top_user": [
    {"_id": "user123", "count": 50}
  ]
}
```

### Note
* Ensure MongoDB is running when the data is ingesting and querying tweets.
* Customize the Data.py script to fit your specific TSV data format if needed.
