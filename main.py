from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import timedelta
from typing import List, Optional
import os

from database import (
    connect_to_mongo, 
    close_mongo_connection,
    db,
    users_collection,
    assets_collection,
    vulnerabilities_collection,
    phi_risks_collection,
    anomalies_collection,
    compliance_collection
)
from auth_utils import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)

app = FastAPI(title="HealthSecure API", description="Healthcare Security Dashboard Backend")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = await users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

# Dependency to check if user is admin
async def get_current_admin(user = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Helper to convert MongoDB document to dict with string ID
def doc_to_dict(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

# Auth endpoints
@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user.get("role", "user")},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {"username": user["username"], "role": user.get("role", "user")}
    }

@app.post("/auth/register")
async def register(username: str, email: str, password: str):
    # Check if user exists
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email exists
    existing_email = await users_collection.find_one({"email": email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create new user
    hashed_password = get_password_hash(password)
    user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "role": "user"  # Default role
    }
    
    await users_collection.insert_one(user)
    return {"message": "User created successfully"}

# Dashboard endpoint
@app.get("/dashboard/stats")
async def get_dashboard_stats(user = Depends(get_current_user)):
    # Get counts
    total_vulns = await vulnerabilities_collection.count_documents({})
    critical_vulns = await vulnerabilities_collection.count_documents({"severity": "Critical"})
    total_assets = await assets_collection.count_documents({})
    critical_assets = await assets_collection.count_documents({"criticality": "Critical"})
    
    # Calculate security score (simplified)
    security_score = 100 - (critical_vulns * 5)
    if security_score < 0:
        security_score = 0
    
    return {
        "security_score": security_score,
        "critical_vulnerabilities": critical_vulns,
        "total_assets": total_assets,
        "critical_assets": critical_assets
    }

# Assets endpoints
@app.get("/assets/")
async def get_assets(user = Depends(get_current_user)):
    assets = await assets_collection.find().to_list(100)
    return [doc_to_dict(a) for a in assets]

@app.post("/assets/")
async def create_asset(asset: dict, user = Depends(get_current_admin)):
    result = await assets_collection.insert_one(asset)
    asset["_id"] = str(result.inserted_id)
    return asset

# Vulnerabilities endpoints
@app.get("/vulnerabilities/")
async def get_vulnerabilities(user = Depends(get_current_user)):
    vulns = await vulnerabilities_collection.find().to_list(100)
    return [doc_to_dict(v) for v in vulns]

@app.post("/vulnerabilities/")
async def create_vulnerability(vuln: dict, user = Depends(get_current_user)):
    result = await vulnerabilities_collection.insert_one(vuln)
    vuln["_id"] = str(result.inserted_id)
    return vuln

@app.put("/vulnerabilities/{vuln_id}")
async def update_vulnerability(vuln_id: str, status: str = None, user = Depends(get_current_user)):
    update_data = {}
    if status:
        update_data["status"] = status
    
    result = await vulnerabilities_collection.update_one(
        {"_id": ObjectId(vuln_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return {"message": "Updated successfully"}

@app.delete("/vulnerabilities/{vuln_id}")
async def delete_vulnerability(vuln_id: str, user = Depends(get_current_admin)):
    result = await vulnerabilities_collection.delete_one({"_id": ObjectId(vuln_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return {"message": "Deleted successfully"}

# PHI Risks endpoints
@app.get("/phi-risks/")
async def get_phi_risks(user = Depends(get_current_user)):
    risks = await phi_risks_collection.find().to_list(100)
    return [doc_to_dict(r) for r in risks]

# Anomalies endpoints
@app.get("/anomalies/")
async def get_anomalies(user = Depends(get_current_user)):
    anomalies = await anomalies_collection.find().to_list(100)
    return [doc_to_dict(a) for a in anomalies]

# Compliance endpoints
@app.get("/compliance/")
async def get_compliance(user = Depends(get_current_user)):
    items = await compliance_collection.find().to_list(100)
    return [doc_to_dict(c) for c in items]

# Seed data endpoint (for initial setup)
@app.post("/seed/")
async def seed_database(force: bool = False):
    """Seed the database with sample data"""
    # Check if data already exists (unless force=true)
    if not force and await assets_collection.count_documents({}) > 0:
        return {"message": "Database already seeded"}
    
    # Clear existing data if force=true
    if force:
        await users_collection.delete_many({})
        await assets_collection.delete_many({})
        await vulnerabilities_collection.delete_many({})
        await phi_risks_collection.delete_many({})
        await anomalies_collection.delete_many({})
        await compliance_collection.delete_many({})
    
    # Sample assets
    assets = [
        {"name": "Patient Database Server", "type": "server", "criticality": "Critical", "status": "Active"},
        {"name": "MRI Scanner Workstation", "type": "workstation", "criticality": "High", "status": "Active"},
        {"name": "Hospital LAN Switch", "type": "network", "criticality": "Critical", "status": "Active"},
    ]
    await assets_collection.insert_many(assets)
    
    # Sample vulnerabilities
    vulns = [
        {"title": "SQL Injection in Patient Portal", "severity": "Critical", "cvss_score": 9.8, "status": "Open", "asset_name": "Patient Database Server"},
        {"title": "Outdated OpenSSL Version", "severity": "High", "cvss_score": 7.5, "status": "Open", "asset_name": "MRI Scanner Workstation"},
        {"title": "Weak Password Policy", "severity": "Medium", "cvss_score": 5.3, "status": "Open", "asset_name": "Hospital LAN Switch"},
    ]
    await vulnerabilities_collection.insert_many(vulns)
    
    # Sample PHI risks
    phi_risks = [
        {"title": "Unencrypted PHI Storage", "severity": "Critical", "description": "Patient data stored without encryption"},
        {"title": "Unauthorized Access Attempt", "severity": "High", "description": "Multiple failed login attempts detected"},
    ]
    await phi_risks_collection.insert_many(phi_risks)
    
    # Sample anomalies
    anomalies = [
        {"title": "Unusual Data Transfer", "description": "Large data transfer to external IP", "severity": "High"},
        {"title": "Login Outside Business Hours", "description": "Admin login at 3 AM", "severity": "Medium"},
    ]
    await anomalies_collection.insert_many(anomalies)
    
    # Sample compliance items
    compliance_items = [
        {"regulation": "HIPAA", "requirement": "Encryption of PHI at rest", "status": "compliant"},
        {"regulation": "HIPAA", "requirement": "Access controls", "status": "compliant"},
        {"regulation": "HIPAA", "requirement": "Audit logging", "status": "non-compliant"},
    ]
    await compliance_collection.insert_many(compliance_items)
    
    # Create default admin user
    admin_user = {
        "username": "admin",
        "email": "admin@healthsecure.com",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin"
    }
    await users_collection.insert_one(admin_user)
    
    # Create default user
    regular_user = {
        "username": "user",
        "email": "user@healthsecure.com",
        "hashed_password": get_password_hash("user123"),
        "role": "user"
    }
    await users_collection.insert_one(regular_user)
    
    return {"message": "Database seeded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
