from pymongo import MongoClient
import os

# ============================================
# MONGODB CONNECTION SETUP
# ============================================
# Option 1 - Local MongoDB (default):
#   MONGO_URL = "mongodb://localhost:27017"
#
# Option 2 - MongoDB Atlas (Cloud):
#   Get your connection string from MongoDB Atlas:
#   1. Go to https://www.mongodb.com/cloud/atlas
#   2. Create a free cluster
#   3. Click "Connect" > "Connect your application"
#   4. Copy the connection string
#   It looks like: mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/
#
#   Replace <username> and <password> with your credentials
#   Replace <cluster> with your cluster name
# ============================================

# Use environment variable or default to local MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["healthsecure"]

assets_collection = db["assets"]
vulnerabilities_collection = db["vulnerabilities"]
phi_risks_collection = db["phi_risks"]
compliance_collection = db["compliance_controls"]
anomalies_collection = db["anomalies"]
users_collection = db["users"]

# Export db for use in other modules
__all__ = ['db', 'assets_collection', 'vulnerabilities_collection', 'phi_risks_collection', 'compliance_collection', 'anomalies_collection', 'users_collection']
