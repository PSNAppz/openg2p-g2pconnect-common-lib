from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from .common import RequestStatusEnum, SingleCommonRequest


class UnlinkStatusReasonCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_beneficiary_name_invalid = "rjct.beneficiary_name.invalid"


class SingleUnlinkRequest(SingleCommonRequest):
    reference_id: str
    timestamp: str
    id: str
    fa: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    additional_info: Optional[List[dict]]
    locale: Optional[str]


class UnlinkRequest(BaseModel):
    transaction_id: str
    unlink_request: List[SingleUnlinkRequest]


class SingleUnlinkResponse(SingleCommonRequest):
    reference_id: str
    timestamp: str
    id: Optional[str] = ""
    status: RequestStatusEnum
    status_reason_code: Optional[UnlinkStatusReasonCode] = None
    status_reason_message: Optional[str] = ""
    additional_info: Optional[List[dict]]
    locale: str


class UnlinkResponse(BaseModel):
    transaction_id: str
    correlation_id: Optional[str] = ""
    unlink_response: List[SingleUnlinkResponse]
