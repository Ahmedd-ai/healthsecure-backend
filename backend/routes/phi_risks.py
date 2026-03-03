from fastapi import APIRouter
from backend.database import db

router = APIRouter(prefix="/api/phi-risks", tags=["PHI Risks"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def get_phi_risks():
    """Get all PHI risks"""
    phi_risks = list(db["phi_risks"].find())
    return [serialize_doc(p) for p in phi_risks]

@router.get("/{phi_risk_id}")
def get_phi_risk(phi_risk_id: int):
    """Get a single PHI risk by ID"""
    phi_risk = db["phi_risks"].find_one({"id": phi_risk_id})
    if not phi_risk:
        return {"error": "PHI risk not found"}
    return serialize_doc(phi_risk)

@router.post("/")
def create_phi_risk(phi_risk: dict):
    """Create a new PHI risk"""
    result = db["phi_risks"].insert_one(phi_risk)
    return {"id": str(result.inserted_id), "message": "PHI risk created"}

@router.put("/{phi_risk_id}")
def update_phi_risk(phi_risk_id: int, phi_risk: dict):
    """Update a PHI risk"""
    result = db["phi_risks"].update_one({"id": phi_risk_id}, {"$set": phi_risk})
    if result.matched_count == 0:
        return {"error": "PHI risk not found"}
    return {"message": "PHI risk updated"}

@router.delete("/{phi_risk_id}")
def delete_phi_risk(phi_risk_id: int):
    """Delete a PHI risk"""
    result = db["phi_risks"].delete_one({"id": phi_risk_id})
    if result.deleted_count == 0:
        return {"error": "PHI risk not found"}
    return {"message": "PHI risk deleted"}
