from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from openg2p_fastapi_common.models import AsyncResponseStatusEnum


class UpdateStatusReasonCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_beneficiary_name_invalid = "rjct.beneficiary_name.invalid"
    rjct_id_invalid = "rjct.id.invalid"


class SingleUpdateRequest(BaseModel):
    reference_id: str
    timestamp: str
    id: str
    fa: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    additional_info: Optional[List[dict]]
    locale: Optional[str]


class UpdateRequest(BaseModel):
    transaction_id: str
    update_request: List[SingleUpdateRequest]


class SingleUpdateResponse(BaseModel):
    reference_id: str
    timestamp: str
    id: Optional[str] = ""
    status: RequestStatusEnum
    status_reason_code: Optional[UpdateStatusReasonCode] = None
    status_reason_message: Optional[str] = ""
    additional_info: Optional[List[dict]]
    locale: str


class UpdateResponse(BaseModel):
    transaction_id: str
    correlation_id: Optional[str] = ""
    update_response: List[SingleUpdateResponse]
