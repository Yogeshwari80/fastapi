from fastapi import APIRouter
from controllers import CategoryController  # Import Category Controller
from models.CategoryModel import Category, CategoryOut

router = APIRouter()

@router.post("/category/")
async def post_category(category: Category):
    return await CategoryController.addCategory(category)

@router.get("/category/")
async def get_category():
    return await CategoryController.getCategory()
