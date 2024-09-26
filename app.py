from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
from Data import ingest_tsv_to_mongo

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.twitter_db
collection = db.tweets

# Function to query tweets based on term
def query_tweets(term):
    tweets_per_day = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}, "count": {"$sum": 1}}}
    ])

    unique_users = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": "$author_id"}}
    ])
    
    avg_likes = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": None, "average_likes": {"$avg": "$like_count"}}}
    ])

    places = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": "$place_id"}}
    ])
    
    tweet_times = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": {"$hour": "$created_at"}, "count": {"$sum": 1}}}
    ])

    top_user = collection.aggregate([
        {"$match": {"text": {"$regex": term, "$options": "i"}}},
        {"$group": {"_id": "$author_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])

    return {
        "tweets_per_day": list(tweets_per_day),
        "unique_users_count": len(list(unique_users)),
        "average_likes": list(avg_likes),
        "places": list(places),
        "tweet_times": list(tweet_times),
        "top_user": list(top_user)
    }
# Flask route to handle requests
@app.route('/', methods=['GET'])

def get_query_tweets():
    # Giving the term which to be searched 
    results = query_tweets("music")  
    return jsonify(results)

if __name__ == '__main__':
    # Step 1: Ingest TSV file before starting the Flask server
    tsv_file_path = "C:/Users/Ankith/Downloads/correct_twitter_201904.tsv"
    ingest_tsv_to_mongo(tsv_file_path)

    # Step 2: Start the Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)
