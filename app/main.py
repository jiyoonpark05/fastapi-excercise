from fastapi import FastAPI
from app.routes import posts, comments

app = FastAPI()

app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "hello world"}