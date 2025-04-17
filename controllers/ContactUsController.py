from fastapi import HTTPException
from models.ContactUsModel import ContactUs
from config.database import contact_us_collection
from bson import ObjectId

async def save_contact_message(contact_data: ContactUs):
    try:
        contact_dict = contact_data.dict()
        result = await contact_us_collection.insert_one(contact_dict)
        return {"message": "Message sent successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving contact message: {e}")

async def get_all_contact_messages():
    try:
        messages_cursor = contact_us_collection.find()
        messages = []
        async for message in messages_cursor:
            message["_id"] = str(message["_id"])
            messages.append(message)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {e}")

