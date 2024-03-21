from pydantic import AliasChoices, BaseModel, Field
from enum import Enum
from typing import Optional

from .status_codes import StatusEnum


class SyncRequestHeader(BaseModel):
    version: Optional[str] = "1.0.0"
    message_id: str
    message_ts: str
    action: str
    sender_id: str
    sender_uri: Optional[str] = ""
    receiver_id: str = ""
    total_count: int
    is_msg_encrypted: bool = Field(
        validation_alias=AliasChoices("is_msg_encrypted", "is_encrypted"), default=False
    )
    meta: dict = {}


class SyncRequest(BaseModel):
    signature: str
    header: SyncRequestHeader
    message: object


class SyncResponseStatusReasonCodeEnum(Enum):
    rjct_version_invalid = "rjct.version.invalid"
    rjct_message_id_duplicate = "rjct.message_id.duplicate"
    rjct_message_ts_invalid = "rjct.message_ts.invalid"
    rjct_action_invalid = "rjct.action.invalid"
    rjct_action_not_supported = "rjct.action.not_supported"
    rjct_total_count_invalid = "rjct.total_count.invalid"
    rjct_total_count_limit_exceeded = "rjct.total_count.limit_exceeded"
    rjct_errors_too_many = "rjct.errors.too_many"


class SyncResponseHeader(BaseModel):
    version: Optional[str] = "1.0.0"
    message_id: str
    message_ts: str
    action: str
    status: StatusEnum
    status_reason_code: Optional[SyncResponseStatusReasonCodeEnum]
    status_reason_message: Optional[str] = ""
    total_count: Optional[int] = None
    completed_count: Optional[int] = None
    sender_id: Optional[str] = None
    receiver_id: Optional[str] = None
    is_msg_encrypted: Optional[bool] = Field(
        validation_alias=AliasChoices("is_msg_encrypted", "is_encrypted"), default=False
    )
    meta: Optional[dict] = {}


class SyncResponse(BaseModel):
    signature: Optional[str] = None
    header: SyncResponseHeader
    message: object
