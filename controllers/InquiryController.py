from models.InquiryModel import InquiryModel, InquiryOut
from bson import ObjectId
from config.database import inquiry_collection
from fastapi.responses import JSONResponse



async def addInquiry(inquiry: InquiryModel):
    saved_inquiry = await inquiry_collection.insert_one(inquiry.dict())
    return JSONResponse(content={"message": "Inquiry added", "id": str(saved_inquiry.inserted_id)}, status_code=201)


async def getInquiries():
    inquiries = await inquiry_collection.find().to_list(1000)
    
    formatted_inquiries = []
    for inquiry in inquiries:
        inquiry["_id"] = str(inquiry.get("_id", "")) 
       
        inquiry_data = {
            "id": inquiry["_id"],  
            "fullname": inquiry.get("fullname", "Unknown"),
            "email": inquiry.get("email", "unknown@example.com"),
            "phone_number": inquiry.get("phone_number", "0000000000"),
            "message": inquiry.get("message", None),
        }

        formatted_inquiries.append(InquiryOut(**inquiry_data))

    return formatted_inquiries
