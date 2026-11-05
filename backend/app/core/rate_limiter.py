import time
from typing import Dict, List, Tuple
from fastapi import Request, HTTPException, status


class SlidingWindowRateLimiter:
    """
    In-memory Sliding Window Rate Limiter for FastAPI.
    Tracks timestamps of requests per client IP / key within window_seconds.
    Thread-safe and memory-bounded with periodic automatic cleanup.
    """
    def __init__(self, requests_limit: int = 60, window_seconds: int = 60, key_prefix: str = "default"):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix
        self._history: Dict[str, List[float]] = {}
        self._last_cleanup = time.time()

    def _cleanup_expired(self, now: float):
        """Remove keys whose latest request is older than window_seconds."""
        if now - self._last_cleanup < 30.0:
            return
        self._last_cleanup = now
        expired_keys = [
            k for k, timestamps in self._history.items()
            if not timestamps or (now - timestamps[-1] > self.window_seconds)
        ]
        for k in expired_keys:
            self._history.pop(k, None)

    async def __call__(self, request: Request) -> bool:
        now = time.time()
        self._cleanup_expired(now)

        # Extract client IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"

        client_key = f"{self.key_prefix}:{client_ip}"
        timestamps = self._history.setdefault(client_key, [])

        # Filter out timestamps outside window
        window_start = now - self.window_seconds
        valid_timestamps = [t for t in timestamps if t > window_start]
        self._history[client_key] = valid_timestamps

        if len(valid_timestamps) >= self.requests_limit:
            oldest = valid_timestamps[0]
            retry_after = int(max(1, self.window_seconds - (now - oldest)))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Quá nhiều yêu cầu. Vui lòng thử lại sau {retry_after} giây.",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.requests_limit),
                    "X-RateLimit-Remaining": "0"
                }
            )

        valid_timestamps.append(now)
        return True


# Preconfigured Rate Limiters for critical endpoints
auth_rate_limiter = SlidingWindowRateLimiter(requests_limit=10, window_seconds=60, key_prefix="auth_login")
register_rate_limiter = SlidingWindowRateLimiter(requests_limit=5, window_seconds=60, key_prefix="auth_register")
upload_rate_limiter = SlidingWindowRateLimiter(requests_limit=15, window_seconds=60, key_prefix="cv_upload")
ai_matching_rate_limiter = SlidingWindowRateLimiter(requests_limit=20, window_seconds=60, key_prefix="ai_match")

