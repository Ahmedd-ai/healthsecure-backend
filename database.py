from pymongo import MongoClient
import os

# ============================================
# MONGODB CONNECTION SETUP (Local)
# ============================================
# Connect using MongoDB Compass:
#   mongodb://localhost:27017
#
# Make sure MongoDB Server is running locally
# ============================================

# Use local MongoDB for MongoDB Compass
MONGO_URL = "mongodb://localhost:27017"

try:
    # Configure MongoDB client with timeout settings
    client = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
    )
    
    # Test the connection
    client.admin.command('ping')
    print('Successfully connected to MongoDB!')
    
    db = client['healthsecure']
    
except Exception as e:
    print(f'Failed to connect to MongoDB: {e}')
    # Fallback to a basic client without connection test
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['healthsecure']

assets_collection = db['assets']
vulnerabilities_collection = db['vulnerabilities']
phi_risks_collection = db['phi_risks']
compliance_collection = db['compliance_controls']
anomalies_collection = db['anomalies']
users_collection = db['users']

# Export db for use in other modules
__all__ = [
    'db',
    'assets_collection',
    'vulnerabilities_collection',
    'phi_risks_collection',
    'compliance_collection',
    'anomalies_collection',
    'users_collection',
]
