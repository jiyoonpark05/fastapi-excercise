import os
import requests
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
database = client["database"]
posts_collection = database["posts"]
comments_collection = database["comments"]


BASE_URL = "https://jsonplaceholder.typicode.com"

async def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()

async def fetch_store_posts():
    posts = await fetch_data("posts")
    await posts_collection.insert_many(posts)

async def fetch_store_comments():
    comments = await fetch_data("comments")
    await comments_collection.insert_many(comments)

async def main():
    await fetch_store_posts()
    await fetch_store_comments()

# asyncio event loop runs until all tasks in main() are completed
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())