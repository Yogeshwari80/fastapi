from fastapi import APIRouter
from models.ContactUsModel import ContactUs
from controllers.ContactUsController import save_contact_message, get_all_contact_messages

router = APIRouter()

@router.post("/contact-us")
async def create_contact_message(contact_data: ContactUs):
    return await save_contact_message(contact_data)

@router.get("/contact-us")
async def fetch_all_contact_messages():
    return await get_all_contact_messages()
