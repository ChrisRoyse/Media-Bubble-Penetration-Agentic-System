from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class ConsentMiddleware(BaseHTTPMiddleware):
    """Reject requests missing IAB TCF v2 or similar consent string."""

    async def dispatch(self, request: Request, call_next):  # type: ignore
        if not request.headers.get("X-Consent-String"):
            raise HTTPException(451, "Consent required (GDPR/CCPA)")
        return await call_next(request)
