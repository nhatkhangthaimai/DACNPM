import pytest
from httpx import AsyncClient


@pytest.mark.anyio
class TestAuthAPI:
    """
    Test suite for Authentication endpoints (/api/v1/auth) as specified in Section 4.
    """

    async def test_login_success(self, client: AsyncClient):
        """TC-AUTH-01: Valid login returns 200 and access_token."""
        response = await client.post("/api/v1/auth/login", json={
            "email": "nguyenvanan.ai@gmail.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "candidate"
        assert data["email"] == "nguyenvanan.ai@gmail.com"

    async def test_login_invalid_password(self, client: AsyncClient):
        """TC-AUTH-02: Invalid password returns 401 Unauthorized."""
        response = await client.post("/api/v1/auth/login", json={
            "email": "nguyenvanan.ai@gmail.com",
            "password": "wrong_password_xyz"
        })
        assert response.status_code == 401
        assert "chính xác" in response.json()["detail"].lower()

    async def test_login_non_existent_email(self, client: AsyncClient):
        """TC-AUTH-03: Non-existent email returns 401 Unauthorized."""
        response = await client.post("/api/v1/auth/login", json={
            "email": "notfound@example.com",
            "password": "password123"
        })
        assert response.status_code == 401

    async def test_register_candidate_success(self, client: AsyncClient):
        """TC-AUTH-04: Register candidate with valid data returns 200 and token."""
        response = await client.post("/api/v1/auth/register/candidate", json={
            "email": "new.candidate@example.com",
            "password": "securepassword123",
            "full_name": "Lê Văn Cường",
            "phone": "0912345678",
            "title": "Junior Python Dev"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "candidate"
        assert data["email"] == "new.candidate@example.com"
        assert "access_token" in data

    async def test_register_duplicate_email_fails(self, client: AsyncClient):
        """TC-AUTH-05: Duplicate email returns 400 Bad Request."""
        response = await client.post("/api/v1/auth/register/candidate", json={
            "email": "nguyenvanan.ai@gmail.com",
            "password": "password123",
            "full_name": "Trùng Email"
        })
        assert response.status_code == 400
        assert "đã được sử dụng" in response.json()["detail"].lower()

    async def test_register_invalid_email_format(self, client: AsyncClient):
        """TC-AUTH-06: Malformed email returns 422 Unprocessable Entity."""
        response = await client.post("/api/v1/auth/register/candidate", json={
            "email": "not-an-email-format",
            "password": "password123",
            "full_name": "Lỗi Email"
        })
        assert response.status_code == 422
