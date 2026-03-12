from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os

# MongoDB Atlas connection string - MUST be set via environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set")

# Create client with server API
client = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))

# Database and collections
db = client.healthsecure

users_collection = db.users
assets_collection = db.assets
vulnerabilities_collection = db.vulnerabilities
phi_risks_collection = db.phi_risks
anomalies_collection = db.anomalies
compliance_collection = db.compliance

async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def close_mongo_connection():
    """Close MongoDB connection"""
    client.close()
