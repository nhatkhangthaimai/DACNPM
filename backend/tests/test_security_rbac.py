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
