


from config.database import property_collection  # Property Collection
from models.PropertyModel import Property, PropertyOut
from fastapi import APIRouter, HTTPException, UploadFile, File,Form
from fastapi.responses import JSONResponse
from bson import ObjectId
import shutil
import os
from utils.CloudinaryUtil import upload_image
from typing import List, Optional

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
    
# async def getAllProperties():
#     properties = await property_collection.find().to_list(None)
#     print("Properties List: ", properties)
#     return [PropertyOut(**property) for property in properties]
async def getAllProperties():
    properties = await property_collection.find().to_list(None)
    print("Properties List: ", properties)
    
    # Convert _id to string before sending data to PropertyOut
    for property in properties:
        property["_id"] = str(property["_id"])
    
    return [PropertyOut(**property) for property in properties]


async def addProperty(property: Property):
    result = await property_collection.insert_one(property.dict())
    print("Inserted Property ID:", result.inserted_id)
    return {"message": "Property Created Successfully", "id": str(result.inserted_id)}

# async def getPropertyById(propertyId: str):
#     property_data = await property_collection.find_one({"_id": ObjectId(propertyId)})
#     if property_data:
#         return PropertyOut(**property_data)
#     return {"message": "Property Not Found"}

# async def deleteProperty(propertyId: str):
#     result = await property_collection.delete_one({"_id": ObjectId(propertyId)})
#     if result.deleted_count > 0:
#         return {"message": "Property Deleted Successfully"}
#     return {"message": "Property Not Found"}
async def updateProperty(property_id: str, property: Property):
    result = await property_collection.update_one(
        {"_id": ObjectId(property_id)},
        {"$set": property.dict()}
    )
    if result.modified_count:
        return {"message": "Property Updated Successfully"}
    return {"message": "No Property Found or No Changes Made"}

async def deleteProperty(property_id: str):
    result = await property_collection.delete_one({"_id": ObjectId(property_id)})
    if result.deleted_count:
        return {"message": "Property Deleted Successfully"}
    return {"message": "No Property Found"}

async def create_property_with_file(
    property_name: str = Form(...),
    category_id: str = Form(...),
    listing_type: str = Form(...),
    base_price: float = Form(...),
    negotiable: Optional[bool] = Form(None),
    address: str = Form(...),
    state_id: str = Form(...),
    city_id: str = Form(...),
    area_id: Optional[str] = Form(None),
    landmarks: Optional[str] = Form(None),
    maps_link: Optional[str] = Form(None),
    built_up_area: Optional[float] = Form(None),
    carpet_area: Optional[float] = Form(None),
    bedrooms: Optional[int] = Form(None),
    bathrooms: Optional[int] = Form(None),
    balconies: Optional[int] = Form(None),
    furnishing: Optional[str] = Form(None),
    age_of_property: Optional[int] = Form(None),
    floor_no: Optional[int] = Form(None),
    total_floors: Optional[int] = Form(None),
    facing: Optional[str] = Form(None),
    parking_slots: Optional[int] = Form(None),
    amenities: Optional[List[str]] = Form(None),
    image: UploadFile = File(...)
):
    try:
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save the uploaded file
        file_ext = image.filename.split(".")[-1]  # Get file extension
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")  # Rename file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Upload image to cloud storage
        image_url = await upload_image(file_path)

        property_data = {
            "property_name": property_name,
            "category_id": str(ObjectId(category_id)),
            "listing_type": listing_type,
            "base_price": base_price,
            "negotiable": negotiable,
            "address": address,
            "state_id": str(ObjectId(state_id)),
            "city_id": str(ObjectId(city_id)),
            "area_id": area_id,
            "landmarks": landmarks,
            "maps_link": maps_link,
            "built_up_area": built_up_area,
            "carpet_area": carpet_area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "balconies": balconies,
            "furnishing": furnishing,
            "age_of_property": age_of_property,
            "floor_no": floor_no,
            "total_floors": total_floors,
            "facing": facing,
            "parking_slots": parking_slots,
            "amenities": amenities,
            "property_images": [image_url]  # Store image URL
        }
        print(property_data)
        inserted_property = await property_collection.insert_one(property_data)

        return JSONResponse(content={"message": "Property created successfully", "id": str(inserted_property.inserted_id)}, status_code=201)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")