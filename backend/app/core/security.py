import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status

from app.core.config import settings


def create_access_token(subject: str, role: str, expires_minutes: int = 60 * 10) -> str:
    expires_at = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "role": role, "exp": expires_at.isoformat()}
    encoded_payload = _urlsafe_b64encode(json.dumps(payload).encode("utf-8"))
    signature = _sign(encoded_payload)
    return f"{encoded_payload}.{signature}"


def decode_access_token(token: str) -> dict[str, str]:
    try:
        encoded_payload, signature = token.split(".", 1)
    except ValueError as exc:
        raise _unauthorized() from exc

    expected_signature = _sign(encoded_payload)
    if not hmac.compare_digest(signature, expected_signature):
        raise _unauthorized()

    try:
        payload = json.loads(_urlsafe_b64decode(encoded_payload).decode("utf-8"))
    except (json.JSONDecodeError, ValueError) as exc:
        raise _unauthorized() from exc

    expires_at = datetime.fromisoformat(payload["exp"])
    if expires_at < datetime.now(UTC):
        raise _unauthorized()
    return payload


def _sign(encoded_payload: str) -> str:
    digest = hmac.new(settings.secret_key.encode("utf-8"), encoded_payload.encode("utf-8"), hashlib.sha256).digest()
    return _urlsafe_b64encode(digest)


def _urlsafe_b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _urlsafe_b64decode(encoded: str) -> bytes:
    padding = "=" * (-len(encoded) % 4)
    return base64.urlsafe_b64decode(encoded + padding)


def _unauthorized() -> HTTPException:
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증이 필요합니다.")
