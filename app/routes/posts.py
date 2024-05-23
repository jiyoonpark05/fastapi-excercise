from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List, Optional, Dict
from app.models import Post, DBPost
from app.database import posts_collection

router = APIRouter()

# convert MongoDB documents to Pydantic model-compatible dictionaries
def convert_post(post) -> dict:
    return {
        "_id": str(post["_id"]),
        "userId": int(post["userId"]),
        "id": int(post["id"]),
        "title": str(post["title"]),
        "body": str(post["body"])
    }

@router.get("/", response_model=List[Post])
async def get_posts():
    try:
        posts = await posts_collection.find().to_list(100)
        return [convert_post(post) for post in posts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
