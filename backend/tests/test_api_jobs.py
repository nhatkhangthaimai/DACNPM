import pytest
from httpx import AsyncClient


@pytest.mark.anyio
class TestJobsAPI:
    """
    Test suite for Job Management endpoints (/api/v1/jobs).
    """

    async def test_get_jobs_list(self, client: AsyncClient):
        """TC-JOB-01: GET /jobs returns list of published jobs."""
        response = await client.get("/api/v1/jobs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["title"] == "Senior Python Backend Developer"

    async def test_search_jobs_by_keyword(self, client: AsyncClient):
        """TC-JOB-02: GET /jobs?search=Python filters accurately."""
        response = await client.get("/api/v1/jobs?search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "Python" in data[0]["title"]

    async def test_search_jobs_not_found(self, client: AsyncClient):
        """TC-JOB-03: Search non-existent keyword returns empty list."""
        response = await client.get("/api/v1/jobs?search=CompletelyNonExistentKeywordXYZ123")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    async def test_get_job_detail_success(self, client: AsyncClient):
        """TC-JOB-04: GET /jobs/{id} returns job details."""
        response = await client.get("/api/v1/jobs/test-job-1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-job-1"
        assert data["company_name"] == "VNG Corporation"

    async def test_get_job_detail_not_found(self, client: AsyncClient):
        """TC-JOB-05: GET /jobs/{id} with invalid id returns 404."""
        response = await client.get("/api/v1/jobs/non-existent-id")
        assert response.status_code == 404
        assert "không tìm thấy" in response.json()["detail"].lower()

    async def test_create_job_success(self, client: AsyncClient):
        """TC-JOB-06: POST /jobs creates new job."""
        new_job_payload = {
            "title": "Lead Frontend Architect",
            "description": "Architect high-performance web applications using React and Tailwind.",
            "requirements": "React, TypeScript, CSS Architecture.",
            "benefits": "Stock options and flexible hours.",
            "job_type": "full_time",
            "location": "TP.HCM",
            "salary_min": 40000000,
            "salary_max": 60000000,
            "currency": "VND",
            "experience_level": "lead",
            "required_skills": ["React", "TypeScript", "Tailwind CSS"],
            "preferred_skills": ["Figma", "Docker"]
        }
        response = await client.post("/api/v1/jobs", json=new_job_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Lead Frontend Architect"
        assert data["status"] == "published"
        assert "React" in data["required_skills"]
