import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities import CV, Job, Application


@pytest.mark.anyio
class TestAdminAndApplicationsAPI:
    """
    Test suite for Admin operations and Candidate Application lifecycle.
    Covers moderation, user management, application submission, and status updates.
    """

    async def test_admin_list_users(self, client: AsyncClient):
        """TC-ADM-01: Admin can retrieve list of registered users."""
        resp = await client.get("/api/v1/admin/users")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 3  # Admin, recruiter, candidate seeded in conftest
        emails = [u["email"] for u in data]
        assert "admin@hiresense.ai" in emails

    async def test_admin_toggle_user_active_status(self, client: AsyncClient):
        """TC-ADM-02: Admin can deactivate and activate user accounts."""
        # Deactivate candidate
        resp = await client.put("/api/v1/admin/users/test-cand-1/toggle-active")
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

        # Reactivate candidate
        resp2 = await client.put("/api/v1/admin/users/test-cand-1/toggle-active")
        assert resp2.status_code == 200
        assert resp2.json()["is_active"] is True

    async def test_admin_moderate_job_approve_and_reject(self, client: AsyncClient):
        """TC-ADM-03: Admin can moderate jobs (approve or reject with reason)."""
        # Reject job with reason
        resp_reject = await client.put(
            "/api/v1/admin/jobs/test-job-1/moderate?status=rejected&rejection_reason=Yêu+cầu+lương+chưa+rõ+ràng"
        )
        assert resp_reject.status_code == 200
        assert resp_reject.json()["status"] == "rejected"

        # Approve job
        resp_approve = await client.put("/api/v1/admin/jobs/test-job-1/moderate?status=published")
        assert resp_approve.status_code == 200
        assert resp_approve.json()["status"] == "published"

    async def test_candidate_submit_application(self, client: AsyncClient, db_session: AsyncSession):
        """TC-APP-01: Candidate submits job application with CV."""
        # Seed CV
        cv = CV(
            id="app-test-cv-1",
            candidate_id="test-cand-1",
            file_name="my_cv.pdf",
            file_url="/uploads/my_cv.pdf",
            file_size=2048,
            mime_type="application/pdf",
            extraction_status="completed",
            parsed_data={"full_name": "Nguyễn Văn An", "hard_skills": ["Python", "FastAPI"]}
        )
        db_session.add(cv)
        await db_session.commit()

        app_payload = {
            "job_id": "test-job-1",
            "cv_id": "app-test-cv-1",
            "cover_letter": "Tôi rất hào hứng được ứng tuyển vào vị trí này."
        }

        resp = await client.post("/api/v1/applications", json=app_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["job_id"] == "test-job-1"
        assert data["status"] == "submitted"
        assert data["match_score"] is not None
        app_id = data["id"]

        # Recruiter updates application status to reviewing
        resp_status = await client.put(
            f"/api/v1/applications/{app_id}/status",
            json={"status": "reviewing", "internal_notes": "Hồ sơ ứng viên rất tiềm năng."}
        )
        assert resp_status.status_code == 200
        assert resp_status.json()["status"] == "reviewing"
        assert resp_status.json()["internal_notes"] == "Hồ sơ ứng viên rất tiềm năng."
