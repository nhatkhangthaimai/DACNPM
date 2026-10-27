import pytest
from app.ai.pipeline import calculate_hybrid_match


class TestSkillGapAnalysis:
    """
    Test suite for Skill Gap Analysis as specified in Section 8.
    Verifies that the system correctly identifies:
    - Matched Skills
    - Missing Required Skills
    - Missing Preferred Skills
    - Skill Recommendations
    """

    def test_skill_gap_exact_breakdown(self):
        """
        Example from Section 8:
        CV has: Python, FastAPI, PostgreSQL
        JD requires: Python, FastAPI, PostgreSQL, Docker, CI/CD
        Expected:
        - Matched: Python, FastAPI, PostgreSQL
        - Missing: Docker, CI/CD
        - Recommendations present for missing skills
        """
        cv_data = {
            "hard_skills": ["Python", "FastAPI", "PostgreSQL"],
            "experience": [{"job_title": "Backend Dev", "description": "Python FastAPI Postgres services."}]
        }
        job_data = {
            "title": "Backend Engineer",
            "description": "Develop backend with Python, FastAPI, PostgreSQL, Docker, and CI/CD pipelines.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "CI/CD"],
            "preferred_skills": ["Kubernetes"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        # Check matched skills
        assert "Python" in result["matched_skills"]
        assert "FastAPI" in result["matched_skills"]
        assert "PostgreSQL" in result["matched_skills"]

        # Check missing required skills
        assert "Docker" in result["missing_required_skills"]
        assert "CI/CD" in result["missing_required_skills"]
        assert "Kubernetes" in result["missing_preferred_skills"]

        # Check that recommendations address missing skills
        rec_text = " ".join(result["recommendations"])
        assert "Docker" in rec_text
        assert "CI/CD" in rec_text

    def test_skill_gap_with_synonyms(self):
        """
        Check that synonyms (e.g. k8s vs Kubernetes, psql vs PostgreSQL) do NOT falsely trigger missing skills.
        """
        cv_data = {
            "hard_skills": ["python", "k8s", "psql"],
            "experience": []
        }
        job_data = {
            "title": "DevOps Engineer",
            "required_skills": ["Python", "Kubernetes", "PostgreSQL"],
            "preferred_skills": []
        }

        result = calculate_hybrid_match(cv_data, job_data)
        assert len(result["missing_required_skills"]) == 0
        assert len(result["matched_skills"]) == 3

    def test_all_skills_matched_recommendation(self):
        """When candidate meets all skills, recommendation advises direct interview readiness."""
        cv_data = {
            "hard_skills": ["Python", "FastAPI"],
            "experience": [{"job_title": "Dev", "description": "Python FastAPI"}]
        }
        job_data = {
            "title": "Junior Python Dev",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": []
        }

        result = calculate_hybrid_match(cv_data, job_data)
        assert len(result["missing_required_skills"]) == 0
        assert any("hoàn hảo" in r.lower() or "sẵn sàng" in r.lower() for r in result["recommendations"])
