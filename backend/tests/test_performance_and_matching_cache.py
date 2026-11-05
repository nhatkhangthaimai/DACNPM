import pytest
import time
from httpx import AsyncClient
from app.api.v1.endpoints.jobs import extract_job_skills, invalidate_jobs_cache, _JOBS_CACHE


def test_extract_job_skills_performance_and_accuracy():
    """Verify that skill extraction is fast, uses LRU cache and detects keywords."""
    reqs = "Yêu cầu ứng viên thành thạo React, TypeScript, Node.js, Docker và Git."
    desc = "Phát triển hệ thống web quy mô lớn."

    req_skills, pref_skills = extract_job_skills("job-test-perf-1", reqs, desc)
    assert "React" in req_skills
    assert "TypeScript" in req_skills
    assert "Docker" in req_skills
    assert "Git" in req_skills

    # Test cache speed
    t0 = time.perf_counter()
    for _ in range(200):
        extract_job_skills("job-test-perf-1", reqs, desc)
    elapsed = time.perf_counter() - t0
    assert elapsed < 0.05, f"Cached extractions should take < 50ms for 200 calls, took {elapsed*1000:.2f}ms"


def test_jobs_cache_invalidation():
    """Verify in-memory cache storage and invalidation."""
    _JOBS_CACHE["test-cache-key"] = {"data": [{"id": "1"}], "expires_at": time.time() + 100}
    assert len(_JOBS_CACHE) > 0

    invalidate_jobs_cache()
    assert len(_JOBS_CACHE) == 0


@pytest.mark.asyncio
async def test_matching_cache_endpoints(client: AsyncClient):
    """Verify new GET /matching/result and GET /matching/results endpoints."""
    # Query non-existent match result
    resp = await client.get("/api/v1/matching/result?job_id=non-existent-job&cv_id=non-existent-cv")
    assert resp.status_code == 404

    # Query list of match results for a cv
    resp_list = await client.get("/api/v1/matching/results?cv_id=non-existent-cv")
    assert resp_list.status_code == 200
    assert resp_list.json() == []
