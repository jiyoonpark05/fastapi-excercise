from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List, Optional, Dict
from app.models import Post
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
async def get_posts(
    search: Optional[str] = None,
    userId: Optional[int] = None
):
    try:
        query = {}

        # search parameter
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"body": {"$regex": search, "$options": "i"}}
            ]
         # search by userId
        if userId is not None:
            query["userId"] = userId

        posts = await posts_collection.find(query).to_list(length=None)
        return [convert_post(post) for post in posts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    try:
        post_data = post.dict()

        result = await posts_collection.insert_one(post_data)
        
        if result.inserted_id:
            post_data["_id"] = str(result.inserted_id)
            return convert_post(post_data)
        else:
            raise HTTPException(status_code=400, detail="Post creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: str):
    try:
        post = await posts_collection.find_one({"_id": ObjectId(post_id)})
        if post:
            return post
        else:
            raise HTTPException(status_code=404, detail="post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: str, post: Post):
    try:
        post_data: Dict = post.dict(exclude={"userId", "id"})

        result = await posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": post_data}
        )

        if result.modified_count == 1:
            updated_post = await posts_collection.find_one({"_id": ObjectId(post_id)})
            return updated_post
        else:
            raise HTTPException(status_code=404, detail="post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    try:
        result = await posts_collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 1:
            return {"detail": "post " + post_id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail="post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/count", response_model=int)
async def count_posts_for_user(user_id: int):
    try:
        count = await posts_collection.count_documents({"userId": user_id})
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

