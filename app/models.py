from pydantic import BaseModel, Field
from typing import Optional 

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

class DBPost(BaseModel):
    _id: str
    userId: int
    id: int
    title: str
    body: str

class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str