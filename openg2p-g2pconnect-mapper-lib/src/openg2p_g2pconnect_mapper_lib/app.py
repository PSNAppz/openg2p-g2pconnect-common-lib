# ruff: noqa: E402

from .config import Settings

_config = Settings.get_config()
from openg2p_fastapi_common.app import Initializer as BaseInitializer
from .client import (
    MapperLinkService,
    MapperUpdateService,
    MapperUnlinkService,
    MapperResolveService,
)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        MapperLinkService()
        MapperUpdateService()
        MapperUnlinkService()
        MapperResolveService()
