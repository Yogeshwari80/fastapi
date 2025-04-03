import os
import shutil
from fastapi import HTTPException, UploadFile
from bson import ObjectId
from models.PropertyModel import Property
from config.database import property_collection
from utils.CloudinaryUtil import upload_image

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def create_property(property_data: Property):
    try:
        property_data.category_id = ObjectId(property_data.category_id)
        property_data.state_id = ObjectId(property_data.state_id)
        property_data.city_id = ObjectId(property_data.city_id)
        property_data.area_id = ObjectId(property_data.area_id)
        property_data.user_id = ObjectId(property_data.user_id)

        saved_property = await property_collection.insert_one(property_data.dict())
        return {"message": "Property created successfully", "property_id": str(saved_property.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating property: {str(e)}")
    
def validate_object_id(id_value: str):
    if not id_value or not ObjectId.is_valid(id_value):
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {id_value}")
    return ObjectId(id_value)

async def create_property_with_file(
    property_name: str,
    category_id: str,
    listing_type: str,
    base_price: float,
    negotiable: bool,
    address: str,
    state_id: str,
    city_id: str,
    area_id: str,
    user_id: str,
    landmarks: str,
    maps_link: str,
    built_up_area: float,
    carpet_area: float,
    bedrooms: int,
    bathrooms: int,
    balconies: int,
    furnishing: str,
    age_of_property: int,
    facing: str,
    floor_no: int,
    total_floors: int,
    parking_slots: int,
    image: UploadFile
):
    # try:
    #     file_ext = image.filename.split(".")[-1]
    #     file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")

    #     with open(file_path, "wb") as buffer:
    #         shutil.copyfileobj(image.file, buffer)

    #     image_url = await upload_image(file_path)
    try:
        # Validate ObjectIds Before Conversion
        category_id = validate_object_id(category_id)
        state_id = validate_object_id(state_id)
        city_id = validate_object_id(city_id)
        area_id = validate_object_id(area_id)
        user_id = validate_object_id(user_id)

        # File Handling Code Here...
        image_url = await upload_image(image.file)

        property_data = {
            "property_name": property_name,
            "category_id": str(ObjectId(category_id)),
            "listing_type": listing_type,
            "base_price": base_price,
            "negotiable": negotiable,
            "address": address,
            "state_id": str(ObjectId(state_id)),
            "city_id": str(ObjectId(city_id)),
            "area_id": str(ObjectId(area_id)),
            "user_id": str(ObjectId(user_id)),
            "landmarks": landmarks,
            "maps_link": maps_link,
            "built_up_area": built_up_area,
            "carpet_area": carpet_area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "balconies": balconies,
            "furnishing": furnishing,
            "age_of_property": age_of_property,
            "facing": facing,
            "floor_no": floor_no,
            "total_floors": total_floors,
            "parking_slots": parking_slots,
            "image_url": image_url
        }

        inserted_property = await property_collection.insert_one(property_data)
        return {"message": "Property created successfully", "property_id": str(inserted_property.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

async def get_properties():
    properties = await property_collection.find().to_list(None)
    
    for prop in properties:
        prop["_id"] = str(prop["_id"])
        prop["category_id"] = str(prop["category_id"])
        prop["state_id"] = str(prop["state_id"])
        prop["city_id"] = str(prop["city_id"])
        prop["area_id"] = str(prop["area_id"])
        prop["user_id"] = str(prop["user_id"])
    
    return properties


# Update Property API
async def update_property(property_id: str, update_data: dict):
    if not ObjectId.is_valid(property_id):
        raise HTTPException(status_code=400, detail="Invalid property ID")

    update_query = {"$set": update_data}
    result = await property_collection.update_one({"_id": ObjectId(property_id)}, update_query)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Property not found")

    return {"message": "Property updated successfully"}

async def delete_property(property_id: str):
    if not ObjectId.is_valid(property_id):
        raise HTTPException(status_code=400, detail="Invalid property ID")

    result = await property_collection.delete_one({"_id": ObjectId(property_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Property not found")

    return {"message": "Property deleted successfully"}