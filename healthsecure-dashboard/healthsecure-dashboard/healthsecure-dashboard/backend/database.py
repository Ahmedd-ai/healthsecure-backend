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
