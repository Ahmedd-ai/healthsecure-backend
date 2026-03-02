from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================
# Get MongoDB connection string from environment variable
# Set this in Vercel dashboard: Settings > Environment Variables
# Format: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set. Please configure it in Vercel dashboard.")

# Configure MongoDB client with timeout settings
client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
)

# Test the connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")
    raise

db = client["healthsecure"]

assets_collection = db["assets"]
vulnerabilities_collection = db["vulnerabilities"]
phi_risks_collection = db["phi_risks"]
compliance_collection = db["compliance_controls"]
anomalies_collection = db["anomalies"]
users_collection = db["users"]

# Export db for use in other modules
__all__ = ['db', 'assets_collection', 'vulnerabilities_collection', 'phi_risks_collection', 'compliance_collection', 'anomalies_collection', 'users_collection']
