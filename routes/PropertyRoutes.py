from fastapi import APIRouter, Form, UploadFile, File
from controllers import PropertyController
from models.PropertyModel import Property

router = APIRouter()

@router.post("/create_property")
async def create_property(property_data: Property):
    return await PropertyController.create_property(property_data)

@router.post("/create_property_file")
async def create_property_with_file(
    property_name: str = Form(...),
    category_id: str = Form(...),
    listing_type: str = Form(...),
    base_price: float = Form(...),
    negotiable: bool = Form(...),
    address: str = Form(...),
    state_id: str = Form(...),
    city_id: str = Form(...),
    area_id: str = Form(...),
    user_id: str = Form(...),
    landmarks: str = Form(...),
    maps_link: str = Form(...),
    built_up_area: float = Form(...),
    carpet_area: float = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    balconies: int = Form(...),
    furnishing: str = Form(...),
    age_of_property: int = Form(...),
    facing: str = Form(...),
    floor_no: int = Form(...),
    total_floors: int = Form(...),
    parking_slots: int = Form(...),
    image: UploadFile = File(...)
):
    return await PropertyController.create_property_with_file(
        property_name, category_id, listing_type, base_price, negotiable, address, state_id, city_id, area_id, 
        user_id, landmarks, maps_link, built_up_area, carpet_area, bedrooms, bathrooms, balconies, furnishing, 
        age_of_property, facing, floor_no, total_floors, parking_slots, image
    )

@router.get("/get_properties")
async def get_properties():
    return await PropertyController.get_properties()


@router.put("/update_property/{property_id}")
async def update_property(property_id: str, update_data: dict):
    return await PropertyController.update_property(property_id, update_data)

@router.delete("/delete_property/{property_id}")
async def delete_property(property_id: str):
    return await PropertyController.delete_property(property_id)