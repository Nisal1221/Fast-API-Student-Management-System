import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    # Notice: transport=transport replaces app=app
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_register_student():
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser_unique@example.com",
        "password": "strongpassword123"
    }
    transport = ASGITransport(app=app)
    # Notice: transport=transport replaces app=app
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json=payload)
    assert response.status_code in [201, 400]
