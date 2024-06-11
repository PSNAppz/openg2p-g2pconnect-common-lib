import httpx
import logging
import base64
import json
from datetime import datetime

from fastapi import Request
from fastapi.security import HTTPBearer

from .config import Settings
from .schemas import DomainEnum
from .token import TokenService


_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class JWTSignatureValidator(HTTPBearer):
    async def __call__(self, request: Request) -> bool:
        token = await TokenService.get_component().get_token()
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Cookie": f"Authorization={token}",
        }

        request_body = await request.body()
        request_json = json.loads(request_body)
        actual_data = base64.b64encode(request_body).decode("utf-8")
        jwt_signature_data = request.headers.get("Authorization")
        if jwt_signature_data is None:
            return False

        reference_id = request_json.get("header", {}).get("sender_id")
        payload = {
            "id": "string",
            "version": "string",
            "requesttime": datetime.utcnow().isoformat(),
            "metadata": {},
            "request": {
                "jwtSignatureData": jwt_signature_data,
                "actual_data": "",
                "applicationId": _config.auth_application_id,
                "referenceId": reference_id,
                "certificateData": "",
                "validateTrust": True,
                "domain": str(DomainEnum.AUTH),
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                _config.auth_jwt_verify_url,
                json=payload,
                headers=headers,
            )
            response_data = response.json()
            try:
               return response_data["response"]["signatureValid"]
            except KeyError:
                return False
