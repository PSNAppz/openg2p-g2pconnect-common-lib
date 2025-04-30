import base64
import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone, timedelta

import httpx
from fastapi import Request
from fastapi.security import HTTPBearer

from .config import Settings
from .schemas import DomainEnum

_config = Settings.get_config(strict=False)
_logger = logging.getLogger(_config.logging_default_logger_name)


def base64url_encode(input: bytes) -> bytes:
    return base64.urlsafe_b64encode(input).replace(b"=", b"")

jwt_validator_keymanager_token: ContextVar[str] = ContextVar("jwt_validator_keymanager_token", default=None)
jwt_validator_keymanager_token_expiry: ContextVar[datetime] = ContextVar("jwt_validator_keymanager_token_expiry", default=None)


class JWTSignatureValidator(HTTPBearer):
    async def __call__(self, request: Request) -> bool:
        # Get request body and decode to JSON
        request_body = await request.body()
        request_json = json.loads(request_body)

        # Canonicalize JSON using separators and encode to base64url (same as JWT payload encoding)
        canonical_json = json.dumps(request_json, separators=(",", ":")).encode("utf-8")
        actual_data = base64url_encode(canonical_json).decode(
            "utf-8"
        )  # base64url-encoded JSON string

        # Get JWT from header
        jwt_signature_data = request.headers.get("Signature")

        try:
            part1, _, part3 = jwt_signature_data.split(".")
        except Exception:
            _logger.error(
                "Malformed detached JWT format. Expected format: part1..part3"
            )
            return False

        # Reconstruct full JWT
        reconstructed_jwt = f"{part1}.{actual_data}.{part3}"

        reference_id = (
            "PARTNER_"
            + request_json.get("header", {}).get("sender_id").replace("-", "_").upper()
        )

        # Prepare payload for external verification
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": datetime.now().isoformat(),
            "metadata": {},
            "request": {
                "jwtSignatureData": reconstructed_jwt,
                "actualData": actual_data,
                "applicationId": _config.jwt_validate_keymanager_app_id,
                "referenceId": reference_id,
                "certificateData": "",
                "validateTrust": False,
                "domain": str(DomainEnum.AUTH),
            },
        }
        # Send request to external service for verification
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{_config.keymanager_api_base_url}/jwtVerify",
                json=payload,
                cookies={"Authorization": await self.get_keymanager_auth_token()},
            )
            try:
                return response.json()["response"]["signatureValid"]
            except Exception as e:
                _logger.error(f"Error: {e}")
                return False

    async def get_keymanager_auth_token(self):
        km_token = jwt_validator_keymanager_token.get()
        km_t_exp = jwt_validator_keymanager_token_expiry.get()
        if km_token and km_t_exp and km_t_exp > datetime.now(timezone.utc):
            return km_token
        url = _config.keymanager_auth_url
        payload = {
            "client_id": _config.keymanager_auth_client_id,
            "client_secret": _config.keymanager_auth_client_secret,
            "grant_type": "client_credentials",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
        response_data = response.json()
        expires_in = response_data.get("expires_in", 900)
        jwt_validator_keymanager_token_expiry.set(datetime.now(timezone.utc) + timedelta(seconds=expires_in))
        jwt_validator_keymanager_token.set(response_data["access_token"])
        return response_data["access_token"]
