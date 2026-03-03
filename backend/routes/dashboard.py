from fastapi import APIRouter
from backend.database import db
from bson import ObjectId

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    
    # Get counts from each collection
    assets_count = db["assets"].count_documents({})
    vulnerabilities_count = db["vulnerabilities"].count_documents({})
    phi_risks_count = db["phi_risks"].count_documents({})
    compliance_count = db["compliance_controls"].count_documents({})
    anomalies_count = db["anomalies"].count_documents({})
    
    # Get open vulnerabilities by severity
    open_vulns = list(db["vulnerabilities"].find({"status": "Open"}))
    
    # Calculate risk score (mock calculation)
    risk_score = min(100, (vulnerabilities_count * 5) + (phi_risks_count * 3))
    
    return {
        "assets_count": assets_count,
        "vulnerabilities_count": vulnerabilities_count,
        "phi_risks_count": phi_risks_count,
        "compliance_count": compliance_count,
        "anomalies_count": anomalies_count,
        "risk_score": risk_score,
        "open_vulnerabilities": [serialize_doc(v) for v in open_vulns]
    }

@router.get("/recent-activity")
def get_recent_activity():
    """Get recent activity across all categories"""
    
    # Get recent vulnerabilities
    recent_vulns = list(db["vulnerabilities"].find().sort("_id", -1).limit(5))
    
    # Get recent anomalies
    recent_anomalies = list(db["anomalies"].find().sort("_id", -1).limit(5))
    
    return {
        "recent_vulnerabilities": [serialize_doc(v) for v in recent_vulns],
        "recent_anomalies": [serialize_doc(a) for a in recent_anomalies]
    }
