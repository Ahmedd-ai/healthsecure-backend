from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================

# Get MongoDB connection string from environment variable
# Set this in Render dashboard: Environment Variables
# Format: mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority

MONGO_URL = os.getenv("MONGO_URL")

# Initialize client as None initially
client = None
db = None

def get_database():
    """Get the database connection, creating it if necessary."""
    global client, db
    
    if db is not None:
        return db
    
    if not MONGO_URL:
        print("WARNING: MONGO_URL environment variable is not set. Database connection will fail.")
        # Return a mock db object to allow app to start
        return None
    
    try:
        # Configure MongoDB client with timeout settings
        client = MongoClient(
            MONGO_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )
        
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        
        # Get database name from connection string
        db_name = MONGO_URL.split('/')[-1].split('?')[0] if '/' in MONGO_URL else "healthcare"
        db = client[db_name]
        
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas: {e}")
        # Return None to allow app to start (will fail gracefully when accessing data)
        return None

# Try to establish connection at import time
db = get_database()

# If db is None, create placeholder collections to prevent import errors
if db is None:
    # Create placeholder for when MONGO_URL is not set (e.g., during build)
    class PlaceholderCollection:
        def __getattr__(self, name):
            return lambda *args, **kwargs: (print(f"WARNING: Database not connected. {name} operation skipped."), None)[1]
    
    class PlaceholderDB:
        def __getitem__(self, name):
            return PlaceholderCollection()
    
    db = PlaceholderDB()

assets_collection = db["assets"]
vulnerabilities_collection = db["vulnerabilities"]
phi_risks_collection = db["phi_risks"]
compliance_collection = db["compliance_controls"]
anomalies_collection = db["anomalies"]
users_collection = db["users"]

# Export db for use in other modules
__all__ = [
    "db",
    "get_database",
    "assets_collection",
    "vulnerabilities_collection",
    "phi_risks_collection",
    "compliance_collection",
    "anomalies_collection",
    "users_collection",
]
