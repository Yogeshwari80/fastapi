from fastapi import APIRouter
from controllers.InquiryController import addInquiry, getInquiries  
from models.InquiryModel import InquiryBase  
router = APIRouter()

#  Add a new Inquiry
@router.post("/inquiry/")
async def post_inquiry(inquiry: InquiryBase):
    return await addInquiry(inquiry) 
#  Get all Inquiries
@router.get("/inquiry/")
async def get_inquiries():
    return await getInquiries()  
