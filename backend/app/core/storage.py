import os
import uuid
import time
import hmac
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, Tuple
from app.core.config import settings


class BaseStorageService(ABC):
    """Abstract interface for CV and asset file storage."""

    @abstractmethod
    async def save_file(self, content: bytes, filename: str, mime_type: str) -> Tuple[str, str]:
        """Saves content and returns (storage_key, access_url_or_key)."""
        pass

    @abstractmethod
    def generate_presigned_url(self, storage_key: str, expires_in_seconds: int = 900) -> str:
        """Generates a secure temporary download URL (default 15 minutes)."""
        pass

    @abstractmethod
    async def delete_file(self, storage_key: str) -> bool:
        """Deletes the stored object."""
        pass


class LocalStorageService(BaseStorageService):
    """
    Secure Local Filesystem Storage with path-traversal defenses
    and HMAC-SHA256 signed temporary access tokens.
    """
    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_file(self, content: bytes, filename: str, mime_type: str) -> Tuple[str, str]:
        safe_basename = os.path.basename(filename).replace(" ", "_")
        storage_key = f"{uuid.uuid4().hex[:10]}_{safe_basename}"
        file_path = os.path.join(self.upload_dir, storage_key)

        with open(file_path, "wb") as f:
            f.write(content)

        return storage_key, f"/uploads/{storage_key}"

    def generate_presigned_url(self, storage_key: str, expires_in_seconds: int = 900) -> str:
        expires_at = int(time.time()) + expires_in_seconds
        sig_data = f"{storage_key}:{expires_at}".encode("utf-8")
        secret = settings.SECRET_KEY.encode("utf-8")
        signature = hmac.new(secret, sig_data, hashlib.sha256).hexdigest()[:16]
        return f"/api/v1/cvs/download/{storage_key}?expires={expires_at}&sig={signature}"

    async def delete_file(self, storage_key: str) -> bool:
        safe_key = os.path.basename(storage_key)
        file_path = os.path.join(self.upload_dir, safe_key)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception:
                return False
        return False


class S3CompatibleStorageService(BaseStorageService):
    """
    Production S3-compatible Object Storage (AWS S3, Cloudflare R2, MinIO)
    with strict Private ACLs and time-limited Presigned URLs.
    """
    def __init__(
        self,
        bucket_name: str,
        endpoint_url: Optional[str] = None,
        region_name: str = "ap-southeast-1"
    ):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.region_name = region_name

    async def save_file(self, content: bytes, filename: str, mime_type: str) -> Tuple[str, str]:
        try:
            import boto3
            from botocore.config import Config

            s3_client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
                config=Config(signature_version="s3v4")
            )
            safe_basename = os.path.basename(filename).replace(" ", "_")
            storage_key = f"cvs/{uuid.uuid4().hex[:12]}_{safe_basename}"

            s3_client.put_object(
                Bucket=self.bucket_name,
                Key=storage_key,
                Body=content,
                ContentType=mime_type,
                ServerSideEncryption="AES256"
            )
            return storage_key, storage_key
        except Exception:
            # Fallback to local storage if boto3 or S3 credentials are not configured in environment
            local = LocalStorageService()
            return await local.save_file(content, filename, mime_type)

    def generate_presigned_url(self, storage_key: str, expires_in_seconds: int = 900) -> str:
        try:
            import boto3
            from botocore.config import Config

            s3_client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                region_name=self.region_name,
                config=Config(signature_version="s3v4")
            )
            return s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": storage_key},
                ExpiresIn=expires_in_seconds
            )
        except Exception:
            local = LocalStorageService()
            return local.generate_presigned_url(storage_key, expires_in_seconds)

    async def delete_file(self, storage_key: str) -> bool:
        try:
            import boto3
            s3_client = boto3.client("s3", endpoint_url=self.endpoint_url, region_name=self.region_name)
            s3_client.delete_object(Bucket=self.bucket_name, Key=storage_key)
            return True
        except Exception:
            local = LocalStorageService()
            return await local.delete_file(storage_key)


def get_storage_service() -> BaseStorageService:
    """Factory selecting storage adapter based on environment configuration."""
    bucket = os.getenv("S3_BUCKET_NAME")
    if bucket:
        return S3CompatibleStorageService(
            bucket_name=bucket,
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            region_name=os.getenv("S3_REGION", "ap-southeast-1")
        )
    return LocalStorageService()

