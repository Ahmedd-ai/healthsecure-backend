from pymongo import MongoClient
import os

# ============================================
# MONGODB ATLAS CONNECTION (CLOUD)
# ============================================
# MongoDB Atlas connection string
# Format: mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority

# Default connection string - will be used if MONGO_URL env var is not set or invalid
DEFAULT_MONGO_URL = "mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/healthsecure?retryWrites=true&w=majority"

# Get MONGO_URL from environment variable and strip whitespace
env_url = os.environ.get("MONGO_URL", "")
MONGO_URL = env_url.strip() if env_url else DEFAULT_MONGO_URL

# Debug: Print what we got (truncated for security)
print(f"Environment MONGO_URL: '{env_url[:20]}...' (length: {len(env_url)})")
print(f"Using MONGO_URL: '{MONGO_URL[:30]}...'")

# Validate URL starts with mongodb
if not MONGO_URL.startswith("mongodb"):
    print(f"WARNING: Invalid MONGO_URL, using default. Got: '{MONGO_URL[:30]}...'")
    MONGO_URL = DEFAULT_MONGO_URL

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
