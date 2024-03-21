from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .common import (
    AccountProviderInfo,
    RequestStatusEnum,
    SingleCommonRequest,
)
from .message import MsgCallbackHeader, MsgHeader


class ResolveScope(Enum):
    yes_no = "yes_no"
    details = "details"


class ResolveStatusReasonCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_id_invalid = "rjct.id.invalid"
    rjct_fa_invalid = "rjct.fa.invalid"
    rjct_resolve_type_not_supported = "rjct.resolve_type.not_supported"
    succ_fa_active = "succ.fa.active"
    succ_fa_inactive = "succ.fa.inactive"
    succ_fa_not_found = "succ.fa.not_found"
    succ_fa_not_linked_to_id = "succ.fa.not_linked_to_id"
    succ_id_active = "succ.id.active"
    succ_id_inactive = "succ.id.inactive"
    succ_id_not_found = "succ.id.not_found"


class SingleResolveRequest(SingleCommonRequest):
    reference_id: str
    timestamp: str
    fa: Optional[str] = ""
    id: Optional[str] = ""
    name: Optional[str] = None
    scope: Optional[ResolveScope] = ResolveScope.details
    additional_info: Optional[List[object]] = None
    locale: Optional[str] = "en"


class ResolveRequest(BaseModel):
    transaction_id: str
    resolve_request: List[SingleResolveRequest]


class SingleResolveResponse(BaseModel):
    reference_id: str
    timestamp: str
    fa: Optional[str] = None
    id: Optional[str] = None
    account_provider_info: Optional[AccountProviderInfo] = None
    status: RequestStatusEnum
    status_reason_code: Optional[ResolveStatusReasonCode] = None
    status_reason_message: Optional[str] = ""
    additional_info: Optional[List[object]] = None
    locale: Optional[str] = "en"


class ResolveCallbackResponse(BaseModel):
    transaction_id: str
    correlation_id: Optional[str] = ""
    resolve_response: List[SingleResolveResponse]
