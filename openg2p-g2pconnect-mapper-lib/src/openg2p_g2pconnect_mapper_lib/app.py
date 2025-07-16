from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_g2pconnect_common_lib.jwt_helper_service import JWTHelperService

from .client import (
    MapperLinkClient,
    MapperResolveClient,
    MapperUnlinkClient,
    MapperUpdateClient,
)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        MapperLinkClient()
        MapperUpdateClient()
        MapperUnlinkClient()
        MapperResolveClient()
        JWTHelperService()
