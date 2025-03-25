from models.InquiryModel import InquiryBase, InquiryOut
from bson import ObjectId
from config.database import inquiry_collection
from fastapi.responses import JSONResponse
from fastapi import HTTPException



async def addInquiry(inquiry: InquiryBase):
    inquiry_dict = inquiry.dict()
    inquiry_dict["property_id"] = ObjectId(inquiry_dict["property_id"])
    inquiry_dict["user_id"] = ObjectId(inquiry_dict["user_id"])

    saved_inquiry = await inquiry_collection.insert_one(inquiry_dict)
    if not saved_inquiry.inserted_id:
        raise HTTPException(status_code=500, detail="Inquiry could not be added")

    return JSONResponse(content={"message": "Inquiry added successfully"}, status_code=201)



async def getInquiries():
    inquiries = await inquiry_collection.find().to_list(1000)  # Fetch up to 1000 inquiries
    for inquiry in inquiries:
        if "_id" in inquiry and isinstance(inquiry["_id"], ObjectId):
            inquiry["_id"] = str(inquiry["_id"])
        if "property_id" in inquiry and isinstance(inquiry["property_id"], ObjectId):
            inquiry["property_id"] = str(inquiry["property_id"])
        if "user_id" in inquiry and isinstance(inquiry["user_id"], ObjectId):
            inquiry["user_id"] = str(inquiry["user_id"])

    return [InquiryOut(**inquiry) for inquiry in inquiries]
