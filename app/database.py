import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_URL)
database = client["database"]
posts_collection = database["posts"]
comments_collection = database["comments"]