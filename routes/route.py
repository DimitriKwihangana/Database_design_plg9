from fastapi import APIRouter, HTTPException
from mongodbmodel import WaterQuality
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()


@router.get("/mongo/get")
async def get_waterpotability():
    water = list_serial(collection_name.find())
    return water


@router.get("/mongo/get/{id}")
async def get_water_by_id(id: str):
    water = collection_name.find_one({"_id": ObjectId(id)})
    if not water:
        raise HTTPException(status_code=404, detail="Water quality record not found")
    return list_serial([water])[0]


@router.post("/mongo/post")
async def post_water(water: WaterQuality):
    new_water = dict(water)
    result = collection_name.insert_one(new_water)
    return {"_id": str(result.inserted_id), **new_water}

@router.put("/mongo/put/{id}")
async def update_water(id: str, water: WaterQuality):
    updated_water = dict(water)
    result = collection_name.update_one({"_id": ObjectId(id)}, {"$set": updated_water})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Water quality record not found")
    return {"msg": "Water quality record updated successfully"}

# DELETE: Delete a water quality record by ID
@router.delete("/mongo/delete/{id}")
async def delete_water(id: str):
    result = collection_name.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Water quality record not found")
    return {"msg": "Water quality record deleted successfully"}

@router.get("/mongo/get_latest")
async def get_latest_water_record():
    """
    Sorts by ID and get the latest record
    """
    latest_water = collection_name.find().sort("_id", -1).limit(1)
    latest_water = list_serial(latest_water)
    
    if not latest_water:
        raise HTTPException(status_code=404, detail="No water quality records found")
    
    # Extract only the fields required by the model
    filtered_data = {
        "ph": latest_water[0]["ph"],
        "chloramines": latest_water[0]["chloramines"],
        "sulfate": latest_water[0]["sulfate"],
        "conductivity": latest_water[0]["conductivity"],
        "organic_carbon": latest_water[0]["organic_carbon"],
        "trihalomethanes": latest_water[0]["trihalomethanes"],
        "hardness": latest_water[0]["hardness"],
        "solids": latest_water[0]["solids"],
        "turbidity": latest_water[0]["turbidity"],
    }

    return filtered_data

