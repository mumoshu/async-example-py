import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.external_api import ExternalAPIService


# Replace the global client with a fixture
@pytest.fixture
def client():
    app.state.api_service = ExternalAPIService()
    with TestClient(app) as client:
        yield client


# Update test functions to use the fixture
async def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the API Wrapper Example",
        "versions": {"v1": "/v1"},
    }


async def test_get_posts(client):
    response = client.get("/v1/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


async def test_get_post(client):
    response = client.get("/v1/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_get_post_not_found(client):
    response = client.get("/v1/posts/999")
    assert response.status_code == 404


async def test_get_user_posts(client):
    response = client.get("/v1/users/1/posts")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert all(post["userId"] == 1 for post in posts)
