from motor.motor_asyncio import AsyncIOMotorClient

#db url
MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME ="25_internship_fast"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
role_collection = db["roles"]
user_collection = db["users"]

state_collection = db["states"]
city_collection = db["cities"]
area_collection = db["areas"]
category_collection = db["categories"]
sub_category_collection = db["sub_categories"]
# property_collection = db["properties"]
property_collection = db["properties"]
inquiry_collection = db ["inquiries"]