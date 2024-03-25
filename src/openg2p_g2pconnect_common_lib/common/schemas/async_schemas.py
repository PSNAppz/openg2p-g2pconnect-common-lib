from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import AliasChoices, BaseModel, Field

from openg2p_fastapi_common.errors import ErrorResponse
from .status_codes import StatusEnum


class AsyncAck(Enum):
    ACK = "ACK"
    NACK = "NACK"
    ERR = "ERR"


class AsyncResponseStatusReasonCodeEnum(Enum):
    rjct_version_invalid = "rjct.version.invalid"
    rjct_message_id_duplicate = "rjct.message_id.duplicate"
    rjct_message_ts_invalid = "rjct.message_ts.invalid"
    rjct_action_invalid = "rjct.action.invalid"
    rjct_action_not_supported = "rjct.action.not_supported"
    rjct_total_count_invalid = "rjct.total_count.invalid"
    rjct_total_count_limit_exceeded = "rjct.total_count.limit_exceeded"
    rjct_errors_too_many = "rjct.errors.too_many"


class AsyncResponseMessage(BaseModel):
    ack_status: Optional[AsyncAck] = None
    timestamp: datetime
    error: Optional[ErrorResponse] = None
    correlation_id: Optional[str] = None


class AsyncResponse(BaseModel):
    message: AsyncResponseMessage


class AsyncCallbackRequestHeader(BaseModel):
    version: str = "1.0.0"
    message_id: str
    message_ts: str
    action: str
    status: StatusEnum
    status_reason_code: AsyncResponseStatusReasonCodeEnum
    status_reason_message: str
    total_count: int
    completed_count: int
    sender_id: str
    receiver_id: str
    is_msg_encrypted: bool = Field(
        validation_alias=AliasChoices("is_msg_encrypted", "is_encrypted"), default=False
    )
    meta: dict = {}


class AsyncCallbackRequest(BaseModel):
    signature: Optional[str] = None
    header: AsyncCallbackRequestHeader
    message: Optional[object] = None
