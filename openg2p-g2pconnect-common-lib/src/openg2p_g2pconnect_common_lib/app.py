# ruff: noqa: E402

"""Module initializing auth for APIs"""

import asyncio

from .config import Settings

_config = Settings.get_config(strict=False)

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from .token import TokenService


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        # Initialize all Services, Controllers, any utils here.
        TokenService()




