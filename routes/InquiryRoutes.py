  
from fastapi import APIRouter
from controllers import InquiryController 
from models.InquiryModel import InquiryModel, InquiryOut

router = APIRouter()

@router.post("/inquiry/")
async def post_inquiry(inquiry: InquiryModel):
    return await InquiryController.addInquiry(inquiry)

@router.get("/inquiry/")
async def get_inquiries():
    return await InquiryController.getInquiries()

