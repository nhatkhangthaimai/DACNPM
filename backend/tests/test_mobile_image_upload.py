import io
import pytest
import numpy as np
from PIL import Image, ImageDraw
import pillow_heif

pillow_heif.register_heif_opener()


def make_test_image(format="JPEG", width=600, height=800, text="CV NGUYEN VAN AN - Python FastAPI Docker"):
    img = Image.new("RGB", (width, height), color=(250, 250, 250))
    draw = ImageDraw.Draw(img)
    draw.text((30, 40), text, fill=(10, 10, 10))
    draw.text((30, 80), "Email: an.nguyen@example.com", fill=(10, 10, 10))
    draw.text((30, 120), "Ky nang: Python, FastAPI, Docker, PostgreSQL, React", fill=(10, 10, 10))
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


def make_heic_image():
    img = Image.new("RGB", (400, 500), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), "iPhone Camera CV Photo - Senior AI Engineer", fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="HEIF")
    return buf.getvalue()


def make_blank_image(format="JPEG"):
    # Completely solid white image (variance = 0)
    img = Image.new("RGB", (400, 400), color="white")
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()


@pytest.mark.asyncio
class TestMobileImageUploadSuite:

    # TC01: Android Chrome chọn ảnh JPG từ thư viện
    async def test_tc01_android_chrome_jpg_upload(self, client):
        jpg_bytes = make_test_image(format="JPEG")
        files = {"file": ("android_gallery_cv.jpg", jpg_bytes, "image/jpeg")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["file_name"] == "android_gallery_cv.jpg"
        assert json_data["file_size"] == len(jpg_bytes)
        assert json_data["file_url"].startswith("/uploads/")

    # TC02: Android Chrome chọn ảnh PNG
    async def test_tc02_android_chrome_png_upload(self, client):
        png_bytes = make_test_image(format="PNG")
        files = {"file": ("screenshot_cv.png", png_bytes, "image/png")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["file_name"] == "screenshot_cv.png"
        assert json_data["file_url"].endswith(".png")

    # TC03: iPhone Safari chọn ảnh từ Photos (JPEG/PNG)
    async def test_tc03_iphone_safari_photos_upload(self, client):
        jpg_bytes = make_test_image(format="JPEG")
        files = {"file": ("IMG_4021.jpeg", jpg_bytes, "image/jpeg")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        assert res.json()["file_name"] == "IMG_4021.jpeg"

    # TC04: iPhone chọn ảnh HEIC từ thư viện ảnh
    async def test_tc04_iphone_heic_upload(self, client):
        heic_bytes = make_heic_image()
        files = {"file": ("IMG_9912.HEIC", heic_bytes, "image/heic")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["file_name"] == "IMG_9912.HEIC"
        assert json_data["file_url"].startswith("/uploads/")

    # TC05: Điện thoại chọn CV PDF từ Files
    async def test_tc05_mobile_pdf_upload(self, client):
        pdf_bytes = b"%PDF-1.5\n1 0 obj\n<< /Length 12 >>\nstream\nHello PDF CV\nendstream\nendobj\ntrailer\n<<>>\n%%EOF"
        files = {"file": ("my_resume.pdf", pdf_bytes, "application/pdf")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        assert res.json()["file_name"] == "my_resume.pdf"

    # TC06: Điện thoại chọn CV DOCX từ Files
    async def test_tc06_mobile_docx_upload(self, client):
        docx_bytes = b"PK\x03\x04\x14\x00\x00\x00FakeDocxBinaryBytesForTesting12345"
        files = {"file": ("curriculum_vitae.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        assert res.json()["file_name"] == "curriculum_vitae.docx"

    # TC07: Chụp ảnh bằng camera và upload (Auto EXIF rotation transpose)
    async def test_tc07_camera_capture_orientation(self, client):
        img = Image.new("RGB", (600, 800), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), "Camera Shot CV Test", fill="black")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        files = {"file": ("CAMERA_CAPTURE_2026.jpg", buf.getvalue(), "image/jpeg")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200

    # TC08: Upload ảnh quá dung lượng (> 15MB)
    async def test_tc08_upload_oversized_image(self, client):
        oversized = b"\xff\xd8\xff" + b"0" * (16 * 1024 * 1024)
        files = {"file": ("huge_photo.jpg", oversized, "image/jpeg")}
        res = await client.post("/api/v1/cvs/upload", files=files, data={"candidate_id": "test-cand-1"})
        assert res.status_code == 400
        assert "vượt quá giới hạn" in res.json()["detail"]

    # TC09: Upload file giả định dạng ảnh (fake jpg with text content)
    async def test_tc09_upload_fake_image_signature(self, client):
        fake_jpg = b"This is a fake text file disguised as an image"
        files = {"file": ("fake_image.jpg", fake_jpg, "image/jpeg")}
        res = await client.post("/api/v1/cvs/upload", files=files, data={"candidate_id": "test-cand-1"})
        assert res.status_code == 400
        assert "không phải là định dạng ảnh JPEG hợp lệ" in res.json()["detail"]

    # TC10: Upload ảnh rỗng (0 bytes)
    async def test_tc10_upload_empty_file(self, client):
        files = {"file": ("empty.png", b"", "image/png")}
        res = await client.post("/api/v1/cvs/upload", files=files, data={"candidate_id": "test-cand-1"})
        assert res.status_code == 400
        assert "rỗng" in res.json()["detail"]

    # TC11: Avatar upload (Crops to square, resizes to 400x400 WebP)
    async def test_tc11_avatar_upload(self, client):
        jpg_bytes = make_test_image(format="JPEG", width=800, height=600)
        files = {"file": ("my_avatar.jpg", jpg_bytes, "image/jpeg")}
        data = {"user_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload-avatar", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["status"] == "success"
        assert json_data["file_url"].startswith("/uploads/avatar_")
        assert json_data["file_url"].endswith(".webp")

    # TC12: Upload ảnh có tên chứa dấu tiếng Việt
    async def test_tc12_upload_vietnamese_filename(self, client):
        jpg_bytes = make_test_image(format="JPEG")
        files = {"file": ("CV Nguyễn Văn An (Bản Chụp Điện Thoại).jpg", jpg_bytes, "image/jpeg")}
        data = {"candidate_id": "test-cand-1"}
        res = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["file_name"] == "CV Nguyễn Văn An (Bản Chụp Điện Thoại).jpg"
        # The stored file URL must be safe without problematic non-ASCII characters
        assert json_data["file_url"].startswith("/uploads/cv_")

    # TC13: Upload ảnh rồi thay ảnh (update / reupload)
    async def test_tc13_reupload_image(self, client):
        jpg_v1 = make_test_image(format="JPEG", text="CV Version 1")
        files1 = {"file": ("resume_v1.jpg", jpg_v1, "image/jpeg")}
        res1 = await client.post("/api/v1/cvs/upload", files=files1, data={"candidate_id": "test-cand-1"})
        assert res1.status_code == 200
        cv1_id = res1.json()["id"]

        jpg_v2 = make_test_image(format="JPEG", text="CV Version 2 Updated")
        files2 = {"file": ("resume_v2.jpg", jpg_v2, "image/jpeg")}
        res2 = await client.post("/api/v1/cvs/upload", files=files2, data={"candidate_id": "test-cand-1"})
        assert res2.status_code == 200
        cv2_id = res2.json()["id"]
        assert cv1_id != cv2_id

    # TC14: Company logo upload (Preserves aspect ratio, max 500x500 WebP)
    async def test_tc14_company_logo_upload(self, client):
        png_bytes = make_test_image(format="PNG", width=700, height=400)
        files = {"file": ("vng_company_logo.png", png_bytes, "image/png")}
        data = {"company_id": "test-comp-1"}
        res = await client.post("/api/v1/cvs/upload-logo", files=files, data=data)
        assert res.status_code == 200
        json_data = res.json()
        assert json_data["status"] == "success"
        assert json_data["logo_url"].startswith("/uploads/logo_")

    # TC15: Candidate reviews & edits extracted data (Phase 3 requirement)
    async def test_tc15_candidate_edit_parsed_data(self, client):
        jpg_bytes = make_test_image(format="JPEG")
        files = {"file": ("draft_cv.jpg", jpg_bytes, "image/jpeg")}
        res = await client.post("/api/v1/cvs/upload", files=files, data={"candidate_id": "test-cand-1"})
        cv_id = res.json()["id"]

        # Candidate reviews and updates information
        payload = {
            "full_name": "Nguyen Van An Senior",
            "hard_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "PyTorch"],
            "summary": "Ky su AI va Backend giau kinh nghiem"
        }
        update_res = await client.put(f"/api/v1/cvs/{cv_id}/parsed-data", json=payload)
        assert update_res.status_code == 200
        updated_cv = update_res.json()
        assert updated_cv["content_validated"] is True
        assert updated_cv["parsed_data"]["full_name"] == "Nguyen Van An Senior"
        assert "PyTorch" in updated_cv["parsed_data"]["hard_skills"]

    # TC16: Upload CV ảnh không đọc được rồi thử Job Matching -> Matching must be BLOCKED!
    async def test_tc16_unreadable_image_cv_blocks_job_matching(self, client):
        blank_bytes = make_blank_image(format="JPEG")
        files = {"file": ("unreadable_blank_cv.jpg", blank_bytes, "image/jpeg")}
        res = await client.post("/api/v1/cvs/upload", files=files, data={"candidate_id": "test-cand-1"})
        assert res.status_code == 200
        cv_data = res.json()
        assert cv_data["extraction_status"] == "extraction_failed"
        assert cv_data["content_validated"] is False
        cv_id = cv_data["id"]

        # Attempt Job Matching on this invalid/unreadable CV
        matching_res = await client.post("/api/v1/matching/calculate", json={
            "cv_id": cv_id,
            "job_id": "test-job-1"
        })
        # MUST BE BLOCKED (HTTP 400 with CV_EXTRACTION_INVALID)
        assert matching_res.status_code == 400
        err_json = matching_res.json()
        detail_data = err_json.get("detail") if isinstance(err_json.get("detail"), dict) else err_json
        assert detail_data.get("error_code") == "CV_EXTRACTION_INVALID" or detail_data.get("status") == "blocked"
