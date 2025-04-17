from fastapi import APIRouter
from controllers import FavouriteController
from models.FavouriteModel import Favourite


router = APIRouter()

@router.post("/add_favourite")
async def add_favourite(favourite: Favourite):
    return await FavouriteController.add_favourite(favourite)

@router.delete("/remove_favourite/{favourite_id}")
async def remove_favourite(favourite_id: str):
    return await FavouriteController.remove_favourite(favourite_id)

@router.get("/get_favourites/{user_id}")
async def get_favourites_by_user(user_id: str):
    return await FavouriteController.get_favourites_by_user(user_id)


