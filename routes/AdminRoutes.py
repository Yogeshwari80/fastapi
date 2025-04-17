from fastapi import APIRouter
from controllers.AdminController import (
    addAdmin, getAllAdmins, loginAdmin, forgotAdminPassword,
    resetAdminPassword, getAdminById
)
from models.AdminModel import Admin, AdminLogin, ResetAdminPasswordReq

router = APIRouter()

@router.post("/admin/")
async def post_admin(admin: Admin):
    return await addAdmin(admin)

@router.get("/admins/")
async def get_admins():
    return await getAllAdmins()

@router.get("/admin/{adminId}")
async def get_admin_byId(adminId: str):
    return await getAdminById(adminId)

@router.post("/admin/login/")
async def login_admin(admin: AdminLogin):
    return await loginAdmin(admin)

@router.post("/admin/forgotpassword")
async def forgot_password(email: str):
    return await forgotAdminPassword(email)

@router.post("/admin/resetpassword")
async def reset_password(data: ResetAdminPasswordReq):
    return await resetAdminPassword(data)
