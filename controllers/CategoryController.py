from models.CategoryModel import Category, CategoryOut
from bson import ObjectId
from config.database import category_collection
from fastapi.responses import JSONResponse

async def addCategory(category: Category):
    savedCategory = await category_collection.insert_one(category.dict())
    return JSONResponse(content={"message": "Category added"}, status_code=201)

async def getCategory():
    categories = await category_collection.find().to_list(1000)  
    for category in categories:
        if "_id" in category and isinstance(category["_id"], ObjectId):
            category["_id"] = str(category["_id"])  
    return [CategoryOut(**category) for category in categories]