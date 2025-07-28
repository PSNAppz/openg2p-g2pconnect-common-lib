import logging

from openg2p_fastapi_common.helpers import KeymanagerHelper
from openg2p_fastapi_common.service import BaseService

from .config import Settings

_config = Settings.get_config(strict=False)
_logger = logging.getLogger(_config.logging_default_logger_name)


class JWTHelperService(BaseService):
    keymanger_helper: KeymanagerHelper = KeymanagerHelper.get_cached_component()

    def __init__(self, name=""):
        super().__init__(name or _config.default_jwt_helper_name)

    async def verify_jwt(self, orig_jwt: str, payload: dict, **kw) -> bool:
        try:
            return await self.keymanger_helper.verify_jwt(
                orig_jwt,
                payload=payload,
                keymanager_app_id=_config.jwt_validate_keymanager_app_id,
                keymanager_ref_id=self.get_partner_id_from_payload(payload),
                **kw
            )
        except Exception:
            return False

    async def create_jwt_token(self, payload, **kw) -> str:
        return await self.keymanger_helper.create_jwt_token(
            payload,
            keymanager_app_id=_config.jwt_create_keymanager_app_id,
            keymanager_ref_id=_config.jwt_create_keymanager_ref_id,
            **kw
        )

    def get_partner_id_from_payload(self, payload: dict) -> str:
        return "PARTNER_" + payload.get("header", {}).get("sender_id").replace("-", "_").upper()
