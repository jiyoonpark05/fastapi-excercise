from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import Comment
from app.database import comments_collection

router = APIRouter()

def convert_comment(comment) -> dict:
    return {
        "_id": str(comment["_id"]),
        "postId": int(comment["postId"]),
        "id": int(comment["id"]),
        "name": str(comment["name"]),
        "email": str(comment["email"]),
        "body": str(comment["body"])
    }

@router.get("/", response_model=List[Comment])
async def get_comments():
    try:
        comments = await comments_collection.find().to_list(100)
        return [convert_comment(comment) for comment in comments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
