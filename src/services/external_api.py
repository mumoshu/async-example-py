import httpx
from typing import List, Dict, Optional


class ExternalAPIService:
    """Service for interacting with the JSONPlaceholder API."""

    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def get_posts(self) -> List[Dict]:
        """Fetch all posts."""
        response = await self.client.get("/posts")
        response.raise_for_status()
        return response.json()

    async def get_post(self, post_id: int) -> Optional[Dict]:
        """Fetch a specific post by ID."""
        response = await self.client.get(f"/posts/{post_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    async def get_user_posts(self, user_id: int) -> List[Dict]:
        """Fetch all posts from a specific user."""
        response = await self.client.get("/posts", params={"userId": user_id})
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
