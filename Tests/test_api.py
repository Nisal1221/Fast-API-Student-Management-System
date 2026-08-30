import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_register_student():
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json=payload)
    assert response.status_code in [201, 400]  # 201 on new, 400 if already exists
