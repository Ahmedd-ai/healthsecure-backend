from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================

# Get from environment variable (required for production/Render)
# Set MONGO_URL in your environment variables
MONGO_URL = os.getenv("MONGO_URL")

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
    
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    # Fallback to a basic client without connection test
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client["healthcare"]

assets_collection = db["assets"]
vulnerabilities_collection = db["vulnerabilities"]
phi_risks_collection = db["phi_risks"]
compliance_collection = db["compliance_controls"]
anomalies_collection = db["anomalies"]
users_collection = db["users"]

# Export db for use in other modules
__all__ = [
    "db",
    "assets_collection",
    "vulnerabilities_collection",
    "phi_risks_collection",
    "compliance_collection",
    "anomalies_collection",
    "users_collection",
]
