# ruff: noqa: E402

from .config import Settings

_config = Settings.get_config()
from openg2p_fastapi_common.app import Initializer as BaseInitializer
from .client import (
    MapperLinkClient,
    MapperUpdateClient,
    MapperUnlinkClient,
    MapperResolveClient,
)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        MapperLinkClient()
        MapperUpdateClient()
        MapperUnlinkClient()
        MapperResolveClient()
