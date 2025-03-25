from models.InquiryModel import InquiryModel, InquiryOut
from bson import ObjectId
from config.database import inquiry_collection
from fastapi.responses import JSONResponse


# Add an Inquiry
async def addInquiry(inquiry: InquiryModel):
    saved_inquiry = await inquiry_collection.insert_one(inquiry.dict())
    return JSONResponse(content={"message": "Inquiry added", "id": str(saved_inquiry.inserted_id)}, status_code=201)

# Get all Inquiries
# async def getInquiries():
#     inquiries = await inquiry_collection.find().to_list(1000)
    
#     formatted_inquiries = []
#     for inquiry in inquiries:
#         if "_id" in inquiry:
#             inquiry["id"] = str(inquiry.pop("_id"))  # Convert _id to id
        
#         formatted_inquiries.append(InquiryOut(**inquiry))
    
#     return formatted_inquiries
async def getInquiries():
    inquiries = await inquiry_collection.find().to_list(1000)
    
    formatted_inquiries = []
    for inquiry in inquiries:
        inquiry["_id"] = str(inquiry.get("_id", ""))  # Convert ObjectId to string

        # Ensure all required fields are present with default values
        inquiry_data = {
            "id": inquiry["_id"],  # MongoDB `_id` ko `id` me convert kar diya
            "fullname": inquiry.get("fullname", "Unknown"),
            "email": inquiry.get("email", "unknown@example.com"),
            "phone_number": inquiry.get("phone_number", "0000000000"),
            "property_type": inquiry.get("property_type", "Not Specified"),
            "address": inquiry.get("address", "Not Available"),
            "state_id": inquiry.get("state_id", 0),  # Default ID assigned
            "city_id": inquiry.get("city_id", 0),    # Default ID assigned
            "area_id": inquiry.get("area_id", 0),    # Default ID assigned
            "budget": inquiry.get("budget", None),
            "bedrooms": inquiry.get("bedrooms", None),
            "bathrooms": inquiry.get("bathrooms", None),
            "balconies": inquiry.get("balconies", None),
            "furnishing_status": inquiry.get("furnishing_status", None),
            "parking_slot": inquiry.get("parking_slot", None),
            "message": inquiry.get("message", None),
        }

        formatted_inquiries.append(InquiryOut(**inquiry_data))

    return formatted_inquiries
