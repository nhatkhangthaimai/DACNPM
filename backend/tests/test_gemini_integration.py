import os
import pytest
from app.core.config import settings
from app.schemas.all_schemas import CVExtractedData
from app.ai.pipeline import mock_llm_extraction


class TestGeminiAIIntegration:
    """
    Test suite for Google Gemini API integration as specified in Section 6.
    Distinguishes Unit Tests (Pydantic schema validation) from Live Integration Tests.
    Marks Live API calls as BLOCKED if GEMINI_API_KEY is not configured in environment.
    """

    def test_gemini_configuration_and_sdk(self):
        """Test 1: Verify SDK installation and configuration."""
        try:
            import google.generativeai as genai
            sdk_available = True
        except ImportError:
            sdk_available = False

        assert sdk_available, "Google Generative AI SDK must be installed."
        assert settings.GEMINI_MODEL is not None and len(settings.GEMINI_MODEL) > 0, "GEMINI_MODEL must be configured."
        
        # Verify API key is NOT printed or logged, only existence checked
        has_key = bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY.strip()) > 0)
        # Note: In CI/local dev without secrets, this flags status accurately
        print(f"\n[AI Config Status] Model: {settings.GEMINI_MODEL}, Has Key: {has_key}, SDK: {sdk_available}")

    def test_structured_cv_extraction_pydantic_schema(self):
        """Test 2: Verify extracted CV JSON conforms strictly to Pydantic schema."""
        sample_cv_text = """
        NGUYEN VAN AN
        Email: an.nguyen@example.com | Phone: 0908123456
        Kỹ sư AI với kinh nghiệm phát triển hệ thống RAG và LLMs.
        Kỹ năng: Python, PyTorch, FastAPI, PostgreSQL, Docker.
        Kinh nghiệm:
        - AI Solution Lab (2023 - Hiện tại): AI Deployment Engineer.
        Học vấn:
        - Đại học Bách Khoa TP.HCM (2019 - 2023): Kỹ sư Khoa học Máy tính, GPA: 3.6/4.0.
        """

        extracted_data = mock_llm_extraction(sample_cv_text)

        # Validate with Pydantic CVExtractedData
        validated = CVExtractedData(**extracted_data)

        assert validated.full_name is not None
        assert len(validated.hard_skills) > 0
        assert len(validated.education) > 0
        assert len(validated.experience) > 0
        assert "Python" in validated.hard_skills

    def test_live_gemini_api_call(self):
        """
        Test 3: Live Gemini API Call.
        CRITICAL: If GEMINI_API_KEY is not configured, this test is explicitly BLOCKED, NOT PASSED!
        """
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            pytest.skip("BLOCKED: GEMINI_API_KEY is not configured in environment variables. Live API test skipped as BLOCKED.")

        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Minimal test prompt
        response = model.generate_content("Ping. Reply with PONG.")
        assert response.text is not None
        assert len(response.text) > 0
