  
    
    


from models.UserModel import User, UserOut, UserLogin, ResetPasswordReq
from bson import ObjectId
from config.database import user_collection, role_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
from utils.SendMail import send_mail
import datetime
import jwt


async def addUser(user: User):
    user.role_id = ObjectId(user.role_id)
    result = await user_collection.insert_one(user.dict())
    send_mail(user.email, "User Created", "User created successfully")
    return JSONResponse(status_code=201, content={"message": "User created successfully"})


async def getAllUsers():
    users = await user_collection.find().to_list(length=None)
    result = []

    for user in users:
        try:
            if "role_id" in user and isinstance(user["role_id"], ObjectId):
                user["role_id"] = str(user["role_id"])

            if "role_id" in user and isinstance(user["role_id"], str):
                role = await role_collection.find_one({"_id": ObjectId(user["role_id"])})
                if role:
                    role["_id"] = str(role["_id"])
                    user["role"] = role

            user["_id"] = str(user["_id"])
            result.append(UserOut(**user))

        except Exception as e:
            print("Error parsing user:", user)
            print("Exception:", e)

    return result


async def getUserById(userId: str):
    result = await user_collection.find_one({"_id": ObjectId(userId)})
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**result)


async def loginUser(request: UserLogin):
    foundUser = await user_collection.find_one({"email": request.email})

    if foundUser is None:
        raise HTTPException(status_code=404, detail="User not found")

    if "password" in foundUser and bcrypt.checkpw(request.password.encode(), foundUser["password"].encode()):
        foundUser["_id"] = str(foundUser["_id"])
        foundUser["role_id"] = str(foundUser["role_id"])

        role = await role_collection.find_one({"_id": ObjectId(foundUser["role_id"])})
        if role:
            role["_id"] = str(role["_id"])
            foundUser["role"] = role

        return {"message": "User login success", "user": UserOut(**foundUser)}

    raise HTTPException(status_code=401, detail="Invalid password")


SECRET_KEY = "royal"


def generate_token(email: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


async def forgotPassword(email: str):
    foundUser = await user_collection.find_one({"email": email})
    if not foundUser:
        raise HTTPException(status_code=404, detail="Email not found")

    token = generate_token(email)
    resetLink = f"http://localhost:5173/resetpassword/{token}"
    body = f"""
    <html>
        <h1>Hello! This is your password reset link. It expires in 1 hour.</h1>
        <a href="{resetLink}">RESET PASSWORD</a>
    </html>
    """
    send_mail(email, "Reset Password", body)
    return {"message": "Reset link sent successfully"}


async def resetPassword(data: ResetPasswordReq):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token is invalid")

        hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        await user_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return {"message": "Password updated successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="JWT token is invalid")