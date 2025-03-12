


from models.AreaModel import Area, AreaOut
from bson import ObjectId
from config.database import area_collection, city_collection
from fastapi.responses import JSONResponse
from fastapi import HTTPException,APIRouter

router = APIRouter()


async def addArea(area: Area):
    area_dict = area.model_dump()
    saved_area = await area_collection.insert_one(area_dict)
    return JSONResponse(content={"message": "Area added"}, status_code=201)



async def getAreas():
    areas = await area_collection.find().to_list(1000) 
    valid_areas = []
    
    for area in areas:
        if "name" not in area or "city_id" not in area:
            continue  # Skip invalid entries
        
        # Ensure city_id is a string
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])

        # Fetch city details if available
        if "city_id" in area and area["city_id"]:
            try:
                city = await city_collection.find_one({"_id": ObjectId(area["city_id"])})
                if city:
                    city["_id"] = str(city["_id"])  # Convert city ID to string
                    area["city"] = city
            except Exception as e:
                print(f"Error fetching city: {e}")
                area["city"] = None
        else:
            area["city"] = None  # Handle missing city_id case

        if "_id" in area and isinstance(area["_id"], ObjectId):
            area["_id"] = str(area["_id"])  # Convert _id to string
        
        valid_areas.append(area)
    
    return [AreaOut(**area) for area in valid_areas]

async def getAreasByCityId(cityId: str):
    try:
        print(f"Received city_id: {cityId}")
        city_object_id = ObjectId(cityId)
        print(f"Converted city_id to ObjectId: {city_object_id}")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid city_id format")

    city = await city_collection.find_one({"_id": city_object_id})
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    areas = await area_collection.find({"$or": [{"city_id": cityId}, {"city_id": city_object_id}]}).to_list(1000)
    print(f"Fetched areas: {areas}")

    valid_areas = []
    for area in areas:
        if "name" not in area or "city_id" not in area:
            continue  # Skip invalid entries
        
        if "city_id" in area and isinstance(area["city_id"], ObjectId):
            area["city_id"] = str(area["city_id"])

        area["city"] = city  # Attach city details
        
        valid_areas.append(area)
    
    return [AreaOut(**area) for area in valid_areas]



    
@router.get("/area/{cityId}")
async def get_areas_by_city  (cityId: str):
    try:
        areas = await area_collection.find({"city_id": ObjectId(cityId)}).to_list()
        return [AreaOut(**area) for area in areas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

