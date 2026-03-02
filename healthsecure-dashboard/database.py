from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================

# Get MongoDB connection string from environment variable
# Set this in Render dashboard: Environment Variables
# Format: mongodb+srv://<username>:<password>@cluster.mongodb.net/<database>?retryWrites=true&w=majority
# Example: mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/healthcare?retryWrites=true&w=majority

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set. Please configure it in Render dashboard.")

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

# Get database name from connection string or use default
# The database is specified after the slash in the connection string
db_name = MONGO_URL.split('/')[-1].split('?')[0] if '/' in MONGO_URL else "healthcare"
db = client[db_name]

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
