# HIRESENSE AI – BÁO CÁO KẾT QUẢ THỰC THI KIỂM THỬ THỰC TẾ (TEST EXECUTION RESULTS)

**Dự án:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Môi trường thực thi:** Docker Compose on Windows Host  
- Backend Container: Python 3.11.18, FastAPI, PyTest 9.1.1, AnyIO 4.15.1  
- Frontend Container: Nginx Alpine Reverse Proxy, Vite Production Bundle, React 19  
- Database Container: PostgreSQL 16 + pgvector 0.8.7  
**Thời gian thực thi:** 01/11/2026  

---

## 1. TỔNG HỢP KẾT QUẢ KIỂM THỬ (EXECUTIVE SUMMARY)

```text
================================ TEST SUITE SUMMARY ================================
TOTAL TEST CASES:        66 collected
PASSED:                  66 tests (100%)
FAILED:                  0 tests (0%)
BLOCKED / SKIPPED:       0 tests (0%)
WARNINGS:                9 warnings (Pydantic v2 deprecation & upstream library notices)
TOTAL EXECUTION TIME:    78.98 seconds
====================================================================================
```

### Bảng Thống Kê Theo Phân Hệ Kiểm Thử

| Nhóm Kiểm Thử (Test Group) | File Kiểm Thử | Số lượng | PASS | FAIL | BLOCKED | NOT RUN | Tỷ lệ Đạt |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Admin & Applications API** | `test_api_admin_and_apps.py` | 4 | 4 | 0 | 0 | 0 | **100%** |
| **Authentication & Users** | `test_api_auth.py` | 6 | 6 | 0 | 0 | 0 | **100%** |
| **CVs & Matching Endpoints**| `test_api_cvs_and_matching.py` | 7 | 7 | 0 | 0 | 0 | **100%** |
| **Jobs Management API** | `test_api_jobs.py` | 6 | 6 | 0 | 0 | 0 | **100%** |
| **CV & AI Quality Gates** | `test_cv_ai_matching_master.py` | 10 | 10 | 0 | 0 | 0 | **100%** |
| **Gemini AI Integration** | `test_gemini_integration.py` | 3 | 3 | 0 | 0 | 0 | **100%** |
| **Hybrid Job Matching** | `test_hybrid_matching.py` | 6 | 6 | 0 | 0 | 0 | **100%** |
| **Mobile Image & Doc Upload**| `test_mobile_image_upload.py` | 16 | 16 | 0 | 0 | 0 | **100%** |
| **Security & Phân quyền RBAC**| `test_security_rbac.py` | 5 | 5 | 0 | 0 | 0 | **100%** |
| **Skill Gap Analysis** | `test_skill_gap_analysis.py` | 3 | 3 | 0 | 0 | 0 | **100%** |
| **Frontend TypeScript Build** | `tsc -b && vite build` | 1 | 1 | 0 | 0 | 0 | **100%** |
| **Mobile Physical Hardware** | Thiết bị điện thoại thật | 2 | 0 | 0 | 0 | 2 | **NOT RUN** |
| **TỔNG CỘNG** | | **69** | **67** | **0** | **0** | **2** | **97.1%** |

*Ghi chú trung thực: 2 ca kiểm thử vuốt chạm trên thiết bị iPhone và Android vật lý được đánh dấu **NOT RUN** vì môi trường runner không kết nối điện thoại vật lý qua USB/Device Farm.*

---

## 2. KẾT QUẢ THỰC TẾ CHI TIẾT TỪNG CA KIỂM THỬ (66/66 BACKEND TESTS)

```text
tests/test_api_admin_and_apps.py::TestAdminAndApplicationsAPI::test_admin_list_users ......................... PASSED [  1%]
tests/test_api_admin_and_apps.py::TestAdminAndApplicationsAPI::test_admin_toggle_user_active_status ........ PASSED [  3%]
tests/test_api_admin_and_apps.py::TestAdminAndApplicationsAPI::test_admin_moderate_job_approve_and_reject ... PASSED [  4%]
tests/test_api_admin_and_apps.py::TestAdminAndApplicationsAPI::test_candidate_submit_application ............ PASSED [  6%]
tests/test_api_auth.py::TestAuthAPI::test_login_success ..................................................... PASSED [  7%]
tests/test_api_auth.py::TestAuthAPI::test_login_invalid_password ............................................ PASSED [  9%]
tests/test_api_auth.py::TestAuthAPI::test_login_non_existent_email .......................................... PASSED [ 10%]
tests/test_api_auth.py::TestAuthAPI::test_register_candidate_success ........................................ PASSED [ 12%]
tests/test_api_auth.py::TestAuthAPI::test_register_duplicate_email_fails .................................... PASSED [ 13%]
tests/test_api_auth.py::TestAuthAPI::test_register_invalid_email_format ..................................... PASSED [ 15%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_get_cvs_empty_initially ..................... PASSED [ 16%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_upload_cv_invalid_extension_rejected ........ PASSED [ 18%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_upload_cv_valid_pdf_success ................. PASSED [ 19%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_matching_endpoint_calculation ............... PASSED [ 21%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_matching_with_non_existent_cv_returns_404 ... PASSED [ 22%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_delete_cv_success ........................... PASSED [ 24%]
tests/test_api_cvs_and_matching.py::TestCVSAndMatchingAPI::test_set_primary_cv .............................. PASSED [ 25%]
tests/test_api_jobs.py::TestJobsAPI::test_get_jobs_list ..................................................... PASSED [ 27%]
tests/test_api_jobs.py::TestJobsAPI::test_search_jobs_by_keyword ............................................ PASSED [ 28%]
tests/test_api_jobs.py::TestJobsAPI::test_search_jobs_not_found ............................................. PASSED [ 30%]
tests/test_api_jobs.py::TestJobsAPI::test_get_job_detail_success ............................................ PASSED [ 31%]
tests/test_api_jobs.py::TestJobsAPI::test_get_job_detail_not_found .......................................... PASSED [ 33%]
tests/test_api_jobs.py::TestJobsAPI::test_create_job_success ................................................ PASSED [ 34%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc01_valid_pdf_extraction ............ PASSED [ 36%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc02_valid_docx_extraction ........... PASSED [ 37%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc03_corrupted_pdf_rejection ......... PASSED [ 39%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc04_raw_pdf_bytes_quality_gate ...... PASSED [ 40%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc05_empty_cv_rejected ................ PASSED [ 42%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc06_missing_gemini_api_key .......... PASSED [ 43%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc07_gemini_api_failure_handling ..... PASSED [ 45%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc08_correct_job_matching ............ PASSED [ 46%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc09_invalid_cv_matching_blocked ..... PASSED [ 48%]
tests/test_cv_ai_matching_master.py::TestCVAIMatchingMasterSuite::test_tc10_reupload_cv_cache_invalidation .. PASSED [ 50%]
tests/test_gemini_integration.py::TestGeminiAIIntegration::test_gemini_configuration_and_sdk ................ PASSED [ 51%]
tests/test_gemini_integration.py::TestGeminiAIIntegration::test_structured_cv_extraction_pydantic_schema ... PASSED [ 53%]
tests/test_gemini_integration.py::TestGeminiAIIntegration::test_live_gemini_api_call ........................ PASSED [ 54%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc01_python_backend_high_match ................... PASSED [ 56%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc02_frontend_react_high_match .................. PASSED [ 57%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc03_partial_match ............................... PASSED [ 59%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc04_irrelevant_cv_low_match ..................... PASSED [ 60%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc05_empty_skills_detected ...................... PASSED [ 62%]
tests/test_hybrid_matching.py::TestHybridJobMatching::test_tc06_synonym_semantic_matching .................. PASSED [ 63%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc01_android_chrome_jpg_upload .......... PASSED [ 65%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc02_android_chrome_png_upload .......... PASSED [ 66%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc03_iphone_safari_photos_upload ........ PASSED [ 68%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc04_iphone_heic_upload ................. PASSED [ 69%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc05_mobile_pdf_upload .................. PASSED [ 71%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc06_mobile_docx_upload ................. PASSED [ 72%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc07_camera_capture_orientation ......... PASSED [ 74%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc08_upload_oversized_image ............. PASSED [ 75%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc09_upload_fake_image_signature ........ PASSED [ 77%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc10_upload_empty_file .................. PASSED [ 78%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc11_avatar_upload ....................... PASSED [ 80%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc12_upload_vietnamese_filename ......... PASSED [ 81%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc13_reupload_image ...................... PASSED [ 83%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc14_company_logo_upload ................ PASSED [ 84%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc15_candidate_edit_parsed_data .......... PASSED [ 86%]
tests/test_mobile_image_upload.py::TestMobileImageUploadSuite::test_tc16_unreadable_image_cv_blocks_job_matching PASSED [ 87%]
tests/test_security_rbac.py::TestSecurityAndRBAC::test_password_hashing_bcrypt .............................. PASSED [ 89%]
tests/test_security_rbac.py::TestSecurityAndRBAC::test_jwt_token_encode_decode .............................. PASSED [ 90%]
tests/test_security_rbac.py::TestSecurityAndRBAC::test_invalid_token_decode_fails ........................... PASSED [ 92%]
tests/test_security_rbac.py::TestSecurityAndRBAC::test_candidate_forbidden_from_admin_endpoints ............. PASSED [ 93%]
tests/test_security_rbac.py::TestSecurityAndRBAC::test_admin_authorized_for_admin_endpoints ................. PASSED [ 95%]
tests/test_skill_gap_analysis.py::TestSkillGapAnalysis::test_skill_gap_exact_breakdown ....................... PASSED [ 96%]
tests/test_skill_gap_analysis.py::TestSkillGapAnalysis::test_skill_gap_with_synonyms ........................ PASSED [ 98%]
tests/test_skill_gap_analysis.py::TestSkillGapAnalysis::test_all_skills_matched_recommendation .............. PASSED [100%]
```

---

## 3. KẾT QUẢ KIỂM THỬ FRONTEND BUILD & BUNDLING

```text
> frontend@0.0.0 build
> tsc -b && vite build

vite v5.4.21 building for production...
transforming...
✓ 2694 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                   1.23 kB │ gzip:   0.76 kB
dist/assets/index-C_PW1lp-.css   41.59 kB │ gzip:   7.50 kB
dist/assets/index-CtIFsCcC.js   969.93 kB │ gzip: 281.05 kB
✓ built in 11.80s
Status: EXITED WITH CODE 0 (SUCCESSFUL)
```

---

## 4. KẾT QUẢ KIỂM TRA MẠNG & HTTP ENDPOINTS THỰC TẾ

| Endpoint | Giao thức | Target Container | HTTP Status | Response Payload |
|---|---|---|:---:|---|
| `GET /health` | HTTP/1.1 | `hiresense_backend:8000` | **200 OK** | `{"status":"healthy","gemini_model":"gemini-3.5-flash-lite"}` |
| `GET /` | HTTP/1.1 | `hiresense_frontend:5173` | **200 OK** | HTML SPA container (Length: 1230 bytes) |
| `GET /api/v1/jobs` | Nginx Proxy | `frontend:5173 -> backend:8000`| **200 OK** | Danh sách 2 công việc đã publish từ DB |
| `GET /api/v1/docs` | HTTP/1.1 | `hiresense_backend:8000` | **200 OK** | Swagger UI documentation |
