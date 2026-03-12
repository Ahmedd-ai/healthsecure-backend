import asyncio
from database import connect_to_mongo, users_collection, db

async def check_users():
    await connect_to_mongo()
    users = await users_collection.find().to_list(10)
    print("Users in database:")
    for u in users:
        print(f"  - {u.get('username')}: role={u.get('role')}, has_password={'hashed_password' in u}")
    
    # Check if admin exists
    admin = await users_collection.find_one({"username": "admin"})
    print(f"\nAdmin user: {admin}")
    
    await db.client.close()

asyncio.run(check_users())
