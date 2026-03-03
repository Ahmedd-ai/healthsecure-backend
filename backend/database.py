from pymongo import MongoClient
import os

# ============================================
# MONGODB CONNECTION SETUP
# ============================================
# For local development, use: mongodb://localhost:27017
# For production (Render), use MongoDB Atlas connection string
# Set MONGO_URL environment variable on Render
# ============================================

# Check for environment variable first (for production), fallback to local
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

# If MONGO_URL contains "mongodb+srv", it's an Atlas connection
# For Atlas, we don't need the port
if ".net/" in MONGO_URL and "mongodb+srv" in MONGO_URL:
    # Atlas connection - use direct connect for older pymongo
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=10000)
else:
    # Local or other connection
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

try:
    # Test the connection
    client.admin.command('ping')
    print('Successfully connected to MongoDB!')
except Exception as e:
    print(f'Failed to connect to MongoDB: {e}')

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
