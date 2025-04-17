from models.AdminModel import Admin, AdminOut, AdminLogin, ResetAdminPasswordReq
from bson import ObjectId
from config.database import admin_collection, role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.SendMail import send_mail
import datetime
import jwt


async def addAdmin(admin: Admin):
    admin.role_id = ObjectId(admin.role_id)
    result = await admin_collection.insert_one(admin.dict())
    send_mail(admin.email, "Admin Created", "Admin created successfully")
    return JSONResponse(status_code=201, content={"message": "Admin created successfully"})


async def getAllAdmins():
    admins = await admin_collection.find().to_list(length=None)
    result = []

    for admin in admins:
        try:
            if "role_id" in admin and isinstance(admin["role_id"], ObjectId):
                admin["role_id"] = str(admin["role_id"])

            if "role_id" in admin and isinstance(admin["role_id"], str):
                role = await role_collection.find_one({"_id": ObjectId(admin["role_id"])})
                if role:
                    role["_id"] = str(role["_id"])
                    admin["role"] = role

            admin["_id"] = str(admin["_id"])
            result.append(AdminOut(**admin))

        except Exception as e:
            print("Error parsing admin:", admin)
            print("Exception:", e)

    return result


async def getAdminById(adminId: str):
    result = await admin_collection.find_one({"_id": ObjectId(adminId)})
    if not result:
        raise HTTPException(status_code=404, detail="Admin not found")
    return AdminOut(**result)


async def loginAdmin(request: AdminLogin):
    foundAdmin = await admin_collection.find_one({"email": request.email})

    if foundAdmin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    if "password" in foundAdmin and bcrypt.checkpw(request.password.encode(), foundAdmin["password"].encode()):
        foundAdmin["_id"] = str(foundAdmin["_id"])
        foundAdmin["role_id"] = str(foundAdmin["role_id"])

        role = await role_collection.find_one({"_id": ObjectId(foundAdmin["role_id"])})
        if role:
            role["_id"] = str(role["_id"])
            foundAdmin["role"] = role

        return {"message": "Admin login success", "admin": AdminOut(**foundAdmin)}

    raise HTTPException(status_code=401, detail="Invalid password")


SECRET_KEY = "royal"


def generate_token(email: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


async def forgotAdminPassword(email: str):
    foundAdmin = await admin_collection.find_one({"email": email})
    if not foundAdmin:
        raise HTTPException(status_code=404, detail="Email not found")

    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body = f"""
    <html>
        <h1>Hello! This is your admin password reset link. It expires in 1 hour.</h1>
        <a href="{resetLink}">RESET PASSWORD</a>
    </html>
    """
    send_mail(email, "Reset Password", body)
    return {"message": "Reset link sent successfully"}


async def resetAdminPassword(data: ResetAdminPasswordReq):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token is invalid")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        await admin_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return {"message": "Password updated successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="JWT token is invalid")
