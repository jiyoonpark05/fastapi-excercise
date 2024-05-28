import pytest
import asyncio
import pytest_asyncio
from fastapi import Response
from fastapi.testclient import TestClient
from bson import ObjectId
from app.main import app
from app.models import Post


@pytest.fixture(scope="module")
def api_client():
    with TestClient(app) as client:
        yield client

def test_root(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}

@pytest.mark.asyncio
async def test_get_posts(api_client):
    response = api_client.get("posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_post(api_client):
    post_id = "664f283bcb8c2470e940fa39" 
    url = f"/posts/{post_id}"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()["userId"] == 1

@pytest.mark.asyncio
async def test_create_post(api_client):
    dummy_request = Post(
        userId=1,
        id=1, 
        title="Test Post",
        body="Test body",
    ).model_dump()

    response = api_client.post("/posts/", json=dummy_request)

    assert response.status_code == 201
    created_post = response.json()
    assert "id" in created_post
    assert created_post["userId"] == dummy_request["userId"]
    assert created_post["title"] == dummy_request["title"]
    assert created_post["body"] == dummy_request["body"]

@pytest.mark.asyncio
async def test_update_post(api_client):
    post_id = "664f283bcb8c2470e940fa39" 
    url = f"/posts/{post_id}"
    update_post_data = {"userId": 1, "id": 1,"title": "Test Post Update", "body": "Test Post Update Content"}
   
    response = api_client.put(url, json=update_post_data)
    
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["title"] == update_post_data["title"]

