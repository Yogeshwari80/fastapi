


from config.database import property_collection 
from models.PropertyModel import Property, PropertyOut
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from bson import ObjectId
import shutil
import os
from typing import Optional, List
from utils.CloudinaryUtil import upload_image
from controllers.PropertyController import getAllProperties, addProperty, updateProperty, deleteProperty,getPropertyById


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@router.post("/properties/")
async def create_property(property_data: Property):
    return await addProperty(property_data)

@router.get("/properties/")
async def get_properties():
    return await getAllProperties()  


@router.put("/properties/{property_id}")
async def update_property(property_id: str, property_data: Property):
    return await updateProperty(property_id, property_data)

@router.delete("/properties/{property_id}")
async def delete_property(property_id: str):
    return await deleteProperty(property_id)


# @router.get("/properties/{property_id}", response_model=Property)
# def get_property(property_id: str):
#     property_item = getPropertyById(property_id)
#     if not property_item:
#         raise HTTPException(status_code=404, detail="Property not found")
#     return property_item
@router.get("/properties/{property_id}", response_model=PropertyOut)
async def get_property(property_id: str):
    property_item = await getPropertyById(property_id) 
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_item


@router.post("/create_property_with_file")
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
    # amenities: Optional[str] = Form(None),  # Taking as comma-separated string
    image: UploadFile = File(...)
):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

     
        file_ext = image.filename.split(".")[-1]
        file_path = os.path.join(UPLOAD_DIR, f"{ObjectId()}.{file_ext}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

       
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
            "floor_no": floor_no,
            "total_floors": total_floors,
            "facing": facing,
            "parking_slots": parking_slots,
            # "amenities": amenities_list,
            # "property_images": [image_url]
             "property_images": image_url
        }

       
        property_data = {k: v for k, v in property_data.items() if v is not None}

        inserted_property = await property_collection.insert_one(property_data)

        return JSONResponse(
            content={"message": "Property created successfully", "id": str(inserted_property.inserted_id)},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")