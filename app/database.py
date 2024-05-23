import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

client = AsyncIOMotorClient(MONGO_URL)
database = client["database"]
posts_collection = database["posts"]
comments_collection = database["comments"]