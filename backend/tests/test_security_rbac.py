import pytest
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.entities import UserRole


class TestSecurityAndRBAC:
    """
    Test suite for Security, Password Hashing, JWT Tokens and RBAC as specified in Section 10.
    """

    def test_password_hashing_bcrypt(self):
        """TC-SEC-01: Verify bcrypt password hashing is one-way and never plaintext."""
        raw_password = "SuperSecretPassword#2026"
        hashed = get_password_hash(raw_password)

        assert hashed != raw_password, "Password must not be stored in plaintext."
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$"), "Hash must follow standard bcrypt format."
        assert verify_password(raw_password, hashed) is True, "Password verification must succeed for valid password."
        assert verify_password("wrong_password", hashed) is False, "Password verification must fail for invalid password."

    def test_jwt_token_encode_decode(self):
        """TC-SEC-02: Verify JWT token generation and role decoding."""
        user_id = "test-user-uuid-12345"
        role = UserRole.RECRUITER

        token = create_access_token(subject=user_id, role=role)
        assert isinstance(token, str)
        assert len(token) > 20

        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["role"] == role
        assert "exp" in payload

    def test_invalid_token_decode_fails(self):
        """TC-SEC-03: Invalid or tampered token returns None."""
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidpayload.invalidsignature"
        payload = decode_access_token(invalid_token)
        assert payload is None

    @pytest.mark.anyio
    async def test_candidate_forbidden_from_admin_endpoints(self, client):
        """TC-SEC-04: Candidate token accessing Admin endpoint receives 403 Forbidden."""
        cand_token = create_access_token(subject="user-cand-1", role=UserRole.CANDIDATE)
        headers = {"Authorization": f"Bearer {cand_token}"}
        resp = await client.get("/api/v1/admin/users", headers=headers)
        assert resp.status_code == 403
        assert "không có quyền truy cập" in resp.json()["detail"]

    @pytest.mark.anyio
    async def test_admin_authorized_for_admin_endpoints(self, client):
        """TC-SEC-05: Admin token successfully accesses Admin endpoint."""
        admin_token = create_access_token(subject="user-adm-1", role=UserRole.ADMIN)
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = await client.get("/api/v1/admin/users", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    @pytest.mark.anyio
    async def test_unauthenticated_request_blocked_401(self, client):
        """TC-SEC-06: Request with no Authorization header receives 401 Unauthorized."""
        resp = await client.get("/api/v1/admin/users")
        assert resp.status_code == 401
        assert "yêu cầu đăng nhập" in resp.json()["detail"].lower()

    @pytest.mark.anyio
    async def test_password_reset_flow(self, client):
        """TC-SEC-07: Forgot password and reset password flow."""
        from app.core.security import create_password_reset_token

        # 1. Forgot password request (generic message)
        forgot_resp = await client.post("/api/v1/auth/forgot-password", json={"email": "admin@hiresense.ai"})
        assert forgot_resp.status_code == 200
        assert "hướng dẫn đặt lại mật khẩu" in forgot_resp.json()["message"].lower()

        # 2. Reset password with generated token
        valid_token = create_password_reset_token("admin@hiresense.ai")
        reset_resp = await client.post("/api/v1/auth/reset-password", json={
            "token": valid_token,
            "new_password": "NewSecurePassword#2026"
        })
        assert reset_resp.status_code == 200
        assert "thành công" in reset_resp.json()["message"].lower()

        # 3. Invalid token returns 400
        bad_resp = await client.post("/api/v1/auth/reset-password", json={
            "token": "invalid_fake_token",
            "new_password": "AnotherPassword#2026"
        })
        assert bad_resp.status_code == 400

