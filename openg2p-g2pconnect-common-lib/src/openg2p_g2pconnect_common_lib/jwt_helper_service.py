import base64
import logging
from datetime import datetime, timedelta, timezone

import httpx
import orjson
from openg2p_fastapi_common.service import BaseService

from .config import Settings
from .schemas.security import DomainEnum

_config = Settings.get_config(strict=False)
_logger = logging.getLogger(_config.logging_default_logger_name)


class JWTHelperService(BaseService):
    def __init__(self, name=""):
        super().__init__(name)
        self.keymanager_auth_token = ""
        self.keymanager_auth_token_expiry: datetime | None = None

    async def verify_jwt(self, orig_jwt: str, payload: dict) -> bool:
        try:
            part1, _, part3 = orig_jwt.split(".")
        except Exception:
            _logger.error("Malformed detached JWT format. Expected format: part1..part3")
            return False

        # Canonicalize JSON using separators and encode to base64url (same as JWT payload encoding)
        canonical_json = orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
        actual_data = self.base64url_encode(canonical_json)  # base64url-encoded JSON string

        # Reconstruct full JWT
        reconstructed_jwt = f"{part1}.{actual_data}.{part3}"

        reference_id = self.get_partner_id_from_payload(payload)

        # Send request to external service for verification
        async with httpx.AsyncClient() as client:
            cookies = {}
            if _config.keymanager_auth_enabled:
                cookies["Authorization"] = await self.get_keymanager_auth_token()
            response = await client.post(
                f"{_config.keymanager_api_base_url}/jwtVerify",
                json={
                    "id": "string",
                    "version": "string",
                    "requesttime": self.get_current_isotimestamp(),
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
                },
                cookies=cookies,
                timeout=_config.keymanager_api_timeout,
            )
            try:
                return response.json()["response"]["signatureValid"]
            except Exception as e:
                _logger.error(f"Error: {e}")
        return False

    async def create_jwt_token(
        self,
        payload,
        keymanager_app_id="",
        keymanager_ref_id="",
        include_payload=False,
        include_certificate=False,
        include_cert_hash=False,
    ) -> str:
        if isinstance(payload, dict):
            payload = orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
        elif isinstance(payload, str):
            payload = payload.encode()
        cookies = {}
        if _config.keymanager_auth_enabled:
            cookies["Authorization"] = await self.get_keymanager_auth_token()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{_config.keymanager_api_base_url}/jwtSign",
                json={
                    "id": "string",
                    "version": "string",
                    "requesttime": self.get_current_isotimestamp(),
                    "metadata": {},
                    "request": {
                        "dataToSign": self.base64url_encode(payload),
                        "applicationId": keymanager_app_id,
                        "referenceId": keymanager_ref_id,
                        "includePayload": include_payload,
                        "includeCertificate": include_certificate,
                        "includeCertHash": include_cert_hash,
                    },
                },
                cookies=cookies,
                timeout=_config.keymanager_api_timeout,
            )
        _logger.debug("Keymanager JWT Sign API response: %s", response.text)
        response.raise_for_status()
        return ((response.json() or {}).get("response") or {}).get("jwtSignedData")

    async def get_keymanager_auth_token(self) -> str:
        if (
            self.keymanager_auth_token
            and self.keymanager_auth_token_expiry
            and self.keymanager_auth_token_expiry > datetime.now(timezone.utc)
        ):
            return self.keymanager_auth_token
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
        self.keymanager_auth_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        self.keymanager_auth_token = response_data["access_token"]
        return self.keymanager_auth_token

    def get_partner_id_from_payload(self, payload: dict) -> str:
        return "PARTNER_" + payload.get("header", {}).get("sender_id").replace("-", "_").upper()

    def base64url_encode(self, input) -> str:
        return base64.urlsafe_b64encode(input).decode().rstrip("=")

    def get_current_isotimestamp(self) -> str:
        return f'{datetime.now().isoformat(timespec = "milliseconds")}Z'
