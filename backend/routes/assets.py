from fastapi import APIRouter
from backend.database import db
from bson import ObjectId

router = APIRouter(prefix="/api/assets", tags=["Assets"])

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
def get_assets():
    """Get all assets"""
    assets = list(db["assets"].find())
    return [serialize_doc(a) for a in assets]

@router.get("/{asset_id}")
def get_asset(asset_id: int):
    """Get a single asset by ID"""
    asset = db["assets"].find_one({"id": asset_id})
    if not asset:
        return {"error": "Asset not found"}
    return serialize_doc(asset)

@router.post("/")
def create_asset(asset: dict):
    """Create a new asset"""
    result = db["assets"].insert_one(asset)
    return {"id": str(result.inserted_id), "message": "Asset created"}

@router.put("/{asset_id}")
def update_asset(asset_id: int, asset: dict):
    """Update an asset"""
    result = db["assets"].update_one({"id": asset_id}, {"$set": asset})
    if result.matched_count == 0:
        return {"error": "Asset not found"}
    return {"message": "Asset updated"}

@router.delete("/{asset_id}")
def delete_asset(asset_id: int):
    """Delete an asset"""
    result = db["assets"].delete_one({"id": asset_id})
    if result.deleted_count == 0:
        return {"error": "Asset not found"}
    return {"message": "Asset deleted"}
