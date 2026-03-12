import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

async def create_admin():
    MONGODB_URI = "mongodb+srv://ahmed_db:Uloom%40123@cluster0.3i5uuip.mongodb.net/?appName=Cluster0"
    client = AsyncIOMotorClient(MONGODB_URI, server_api=ServerApi('1'))
    db = client.healthsecure
    users_collection = db.users
    
    # Delete any existing users
    await users_collection.delete_many({})
    
    # Create admin user
    from auth_utils import get_password_hash
    admin_user = {
        "username": "admin",
        "email": "admin@healthsecure.com",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin"
    }
    await users_collection.insert_one(admin_user)
    
    # Create regular user
    regular_user = {
        "username": "user",
        "email": "user@healthsecure.com",
        "hashed_password": get_password_hash("user123"),
        "role": "user"
    }
    await users_collection.insert_one(regular_user)
    
    print("Users created successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
