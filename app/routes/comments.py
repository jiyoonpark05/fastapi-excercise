from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId
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
async def get_comments(
    postId: Optional[int] = None,
):
    try:
        query = {}

        # search by postId
        if postId is not None:
            query["postId"] = postId

        comments = await comments_collection.find(query).to_list(length=None)
        return [convert_comment(comment) for comment in comments]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: Comment):
    try:
        comment_data = comment.dict()

        result = await comments_collection.insert_one(comment_data)
        
        if result.inserted_id:
            comment_data["_id"] = str(result.inserted_id)
            return convert_comment(comment_data)
        else:
            raise HTTPException(status_code=400, detail="Post creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(comment_id: str, comment: Comment):
    try:
        comment_data: Dict = comment.dict(exclude={"postId", "id","name","email"})

        result = await comments_collection.update_one(
            {"_id": ObjectId(comment_id)},
            {"$set": comment_data}
        )

        if result.modified_count == 1:
            updated_comment = await comments_collection.find_one({"_id": ObjectId(comment_id)})
            return updated_comment
        else:
            raise HTTPException(status_code=404, detail="post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(comment_id: str):
    try:
        result = await comments_collection.delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count == 1:
            return {"detail": "comment " + comment_id + " deleted"}
        else:
            raise HTTPException(status_code=404, detail="post not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_email}/count", response_model=int)
async def count_comment_for_user(user_email: str):
    try:
        count = await comments_collection.count_documents({"email": user_email})
        return count
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
