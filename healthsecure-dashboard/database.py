from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================
# Get MongoDB connection string from environment variable
# Set this in Vercel or Render dashboard
# Format: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority

MONGO_URL = os.getenv("MONGO_URL")

# Lazy initialization - client is created only when needed
_client = None
_db = None

def get_client():
    """Get or create MongoDB client lazily"""
    global _client
    if _client is None:
        if not MONGO_URL:
            raise ValueError("MONGO_URL environment variable is not set. Please configure it in Vercel/Render dashboard.")
        
        # Configure MongoDB client with timeout settings
        _client = MongoClient(
            MONGO_URL,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
        )
    return _client

def get_db():
    """Get or create database connection lazily"""
    global _db
    if _db is None:
        client = get_client()
        # Test the connection
        try:
            client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas!")
        except Exception as e:
            print(f"Failed to connect to MongoDB Atlas: {e}")
            raise
        _db = client["healthsecure"]
    return _db

# Create a lazy proxy object that defers connection until first access
class LazyDB:
    """Lazy proxy for database - connects only when accessed"""
    def __getitem__(self, key):
        return get_db()[key]
    
    def __getattr__(self, key):
        return getattr(get_db(), key)

# Use lazy proxy - no connection until first access
db = LazyDB()

# Export for use in other modules
__all__ = ['get_db', 'get_client', 'db', 'MONGO_URL']
