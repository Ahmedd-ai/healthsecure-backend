from fastapi import APIRouter
from backend.database import db

router = APIRouter(prefix="/api/anomalies", tags=["Anomalies"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def get_anomalies():
    """Get all anomalies"""
    anomalies = list(db["anomalies"].find())
    return [serialize_doc(a) for a in anomalies]

@router.get("/{anomaly_id}")
def get_anomaly(anomaly_id: int):
    """Get a single anomaly by ID"""
    anomaly = db["anomalies"].find_one({"id": anomaly_id})
    if not anomaly:
        return {"error": "Anomaly not found"}
    return serialize_doc(anomaly)

@router.post("/")
def create_anomaly(anomaly: dict):
    """Create a new anomaly"""
    result = db["anomalies"].insert_one(anomaly)
    return {"id": str(result.inserted_id), "message": "Anomaly created"}

@router.put("/{anomaly_id}")
def update_anomaly(anomaly_id: int, anomaly: dict):
    """Update an anomaly"""
    result = db["anomalies"].update_one({"id": anomaly_id}, {"$set": anomaly})
    if result.matched_count == 0:
        return {"error": "Anomaly not found"}
    return {"message": "Anomaly updated"}

@router.delete("/{anomaly_id}")
def delete_anomaly(anomaly_id: int):
    """Delete an anomaly"""
    result = db["anomalies"].delete_one({"id": anomaly_id})
    if result.deleted_count == 0:
        return {"error": "Anomaly not found"}
    return {"message": "Anomaly deleted"}
