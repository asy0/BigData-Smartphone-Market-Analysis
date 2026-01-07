"""
MongoDB Connection Module
NoSQL Database Connection for Big Data Analytics Project
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env on import
load_dotenv()

def get_mongodb_connection():
    """
    Establish connection to MongoDB (NoSQL database)
    Uses connection string from .env file or localhost as fallback
    """
    try:
        # Try to get connection string from .env
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DB", "bigdata_analytics")
        
        client = MongoClient(mongodb_uri)
        db = client[db_name]
        
        # Test connection
        client.admin.command('ping')
        print("SUCCESS: MongoDB connection successful!")
        print(f"Database: {db_name}\n")
        
        return db
    except Exception as e:
        print("ERROR: Could not connect to MongoDB!")
        print("Reason:", e)
        print("Note: Make sure MongoDB is running or MONGODB_URI is set in .env\n")
        return None

def close_mongodb_connection(client):
    """Close MongoDB connection"""
    if client:
        client.close()
        print("MongoDB connection closed.")
