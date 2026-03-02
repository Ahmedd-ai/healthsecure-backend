from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================

# MongoDB Atlas connection string
# Format:
# mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority

MONGO_URL = "mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/healthsecure?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)
db = client["healthsecure"]

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
