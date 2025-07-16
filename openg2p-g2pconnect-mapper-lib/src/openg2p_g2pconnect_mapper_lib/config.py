from openg2p_g2pconnect_common_lib.config import Settings as BaseSettings
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="g2pconnect_", env_file=".env", extra="allow")

    mapper_api_url: str = "http://localhost:8007/sync"
    mapper_link_path: str = "/link"
    mapper_update_path: str = "/update"
    mapper_resolve_path: str = "/resolve"
    mapper_unlink_path: str = "/unlink"
    mapper_link_url: str = ""
    mapper_update_url: str = ""
    mapper_resolve_url: str = ""
    mapper_unlink_url: str = ""
    mapper_api_timeout: int = 60
    mapper_api_sign_enabled: bool = True
    mapper_api_sign_keymanager_app_id: str = ""
    mapper_api_sign_keymanager_ref_id: str = ""

    @model_validator(mode="after")
    def validate_mapper_configs(self) -> "Settings":
        base_url = self.mapper_api_url.rstrip("/")
        if not self.mapper_link_url:
            self.mapper_link_url = "/".join(base_url, self.mapper_link_path.lstrip("/"))
        if not self.mapper_update_url:
            self.mapper_update_url = "/".join(base_url, self.mapper_update_path.lstrip("/"))
        if not self.mapper_resolve_url:
            self.mapper_resolve_url = "/".join(base_url, self.mapper_resolve_path.lstrip("/"))
        if not self.mapper_unlink_url:
            self.mapper_unlink_url = "/".join(base_url, self.mapper_unlink_path.lstrip("/"))
        return self
