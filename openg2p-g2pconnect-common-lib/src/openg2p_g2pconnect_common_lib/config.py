from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="g2pconnect_", env_file=".env", extra="allow"
    )

    jwt_validate_keymanager_app_id: str = "OpenG2P-SPAR-Mapper"

    keymanager_api_base_url: str = ""
    keymanager_auth_enabled: bool = True
    keymanager_auth_url: str = ""
    keymanager_auth_client_id: str = "spar-mapper"
    keymanager_auth_client_secret: str = ""
