from fastapi import APIRouter
from backend.database import db

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def get_vulnerabilities():
    """Get all vulnerabilities"""
    vulnerabilities = list(db["vulnerabilities"].find())
    return [serialize_doc(v) for v in vulnerabilities]

@router.get("/{vuln_id}")
def get_vulnerability(vuln_id: int):
    """Get a single vulnerability by ID"""
    vulnerability = db["vulnerabilities"].find_one({"id": vuln_id})
    if not vulnerability:
        return {"error": "Vulnerability not found"}
    return serialize_doc(vulnerability)

@router.post("/")
def create_vulnerability(vulnerability: dict):
    """Create a new vulnerability"""
    result = db["vulnerabilities"].insert_one(vulnerability)
    return {"id": str(result.inserted_id), "message": "Vulnerability created"}

@router.put("/{vuln_id}")
def update_vulnerability(vuln_id: int, vulnerability: dict):
    """Update a vulnerability"""
    result = db["vulnerabilities"].update_one({"id": vuln_id}, {"$set": vulnerability})
    if result.matched_count == 0:
        return {"error": "Vulnerability not found"}
    return {"message": "Vulnerability updated"}

@router.delete("/{vuln_id}")
def delete_vulnerability(vuln_id: int):
    """Delete a vulnerability"""
    result = db["vulnerabilities"].delete_one({"id": vuln_id})
    if result.deleted_count == 0:
        return {"error": "Vulnerability not found"}
    return {"message": "Vulnerability deleted"}
