from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from .common import RequestStatusEnum


class SingleLinkRequest(BaseModel):
    reference_id: str
    timestamp: str
    id: str
    fa: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    additional_info: Optional[str] = ""
    locale: Optional[str]


class LinkRequest(BaseModel):
    transaction_id: str
    link_request: List[SingleLinkRequest]


class LinkStatusReasonCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_id_invalid = "rjct.id.invalid"
    rjct_fa_invalid = "rjct.fa.invalid"
    rjct_name_invalid = "rjct.name.invalid"
    rjct_mobile_number_invalid = "rjct.mobile_number.invalid"
    rjct_unknown_retry = "rjct.unknown.retry"
    rjct_other_error = "rjct.other.error"


class SingleLinkResponse(BaseModel):
    reference_id: str
    timestamp: str
    fa: Optional[str]
    status: RequestStatusEnum
    status_reason_code: Optional[LinkStatusReasonCode]
    status_reason_message: Optional[str]
    additional_info: List[dict]
    locale: str


class LinkResponse(BaseModel):
    transaction_id: str
    correlation_id: str
    link_response: List[SingleLinkResponse]
