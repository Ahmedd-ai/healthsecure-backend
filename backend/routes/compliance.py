from fastapi import APIRouter
from backend.database import db

router = APIRouter(prefix="/api/compliance", tags=["Compliance"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def get_compliance():
    """Get all compliance controls"""
    compliance = list(db["compliance_controls"].find())
    return [serialize_doc(c) for c in compliance]

@router.get("/{compliance_id}")
def get_compliance_item(compliance_id: int):
    """Get a single compliance control by ID"""
    compliance = db["compliance_controls"].find_one({"id": compliance_id})
    if not compliance:
        return {"error": "Compliance control not found"}
    return serialize_doc(compliance)

@router.post("/")
def create_compliance(compliance: dict):
    """Create a new compliance control"""
    result = db["compliance_controls"].insert_one(compliance)
    return {"id": str(result.inserted_id), "message": "Compliance control created"}

@router.put("/{compliance_id}")
def update_compliance(compliance_id: int, compliance: dict):
    """Update a compliance control"""
    result = db["compliance_controls"].update_one({"id": compliance_id}, {"$set": compliance})
    if result.matched_count == 0:
        return {"error": "Compliance control not found"}
    return {"message": "Compliance control updated"}

@router.delete("/{compliance_id}")
def delete_compliance(compliance_id: int):
    """Delete a compliance control"""
    result = db["compliance_controls"].delete_one({"id": compliance_id})
    if result.deleted_count == 0:
        return {"error": "Compliance control not found"}
    return {"message": "Compliance control deleted"}
