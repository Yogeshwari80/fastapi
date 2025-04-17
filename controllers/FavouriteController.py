from fastapi import HTTPException
from bson import ObjectId
from config.database import favourite_collection
from models.FavouriteModel import Favourite

async def add_favourite(favourite: Favourite):
    try:
        favourite_data = {
            "user_id": ObjectId(favourite.user_id),
            "property_id": ObjectId(favourite.property_id),
            "added_date": favourite.added_date
        }
        result = await favourite_collection.insert_one(favourite_data)
        return {"message": "Property added to favourites", "favourite_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding favourite: {str(e)}")

async def remove_favourite(favourite_id: str):
    try:
        result = await favourite_collection.delete_one({"_id": ObjectId(favourite_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Favourite not found")
        return {"message": "Favourite removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing favourite: {str(e)}")

async def get_favourites_by_user(user_id: str):
    try:
        favourites_cursor = favourite_collection.find({"user_id": ObjectId(user_id)})
        favourites = []
        async for fav in favourites_cursor:
            fav["_id"] = str(fav["_id"])  # Convert ObjectId to string
            fav["user_id"] = str(fav["user_id"])
            fav["property_id"] = str(fav["property_id"])
            favourites.append(fav)
        return favourites
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching favourites: {str(e)}")

