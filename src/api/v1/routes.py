from fastapi import APIRouter, HTTPException
from fastapi.requests import Request

router = APIRouter()


@router.get("/posts")
async def get_posts(request: Request):
    """Get all posts from the external API."""
    api_service = request.app.state.api_service
    return await api_service.get_posts()


@router.get("/posts/{post_id}")
async def get_post(post_id: int, request: Request):
    """Get a specific post by ID."""
    api_service = request.app.state.api_service
    post = await api_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, request: Request):
    """Get all posts from a specific user."""
    api_service = request.app.state.api_service
    posts = await api_service.get_user_posts(user_id)
    if not posts:
        raise HTTPException(
            status_code=404,
            detail="No posts found for this user",
        )
    return posts
