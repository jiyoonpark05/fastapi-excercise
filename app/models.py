from pydantic import BaseModel, Field
from typing import Optional 

class Post(BaseModel):
    _id: str
    userId: int
    id: int
    title: str
    body: str

class Comment(BaseModel):
    _id:str
    postId: int
    id: int
    name: str
    email: str
    body: str