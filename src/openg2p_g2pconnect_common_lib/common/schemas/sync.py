from pydantic import AliasChoices, BaseModel, Field
from enum import Enum


class SyncRequestHeader(BaseModel):
    version: str = "1.0.0"
    message_id: str
    message_ts: str
    action: str
    sender_id: str
    sender_uri: str = ""
    receiver_id: str = ""
    total_count: int
    is_msg_encrypted: bool = Field(
        validation_alias=AliasChoices("is_msg_encrypted", "is_encrypted"), default=False
    )
    meta: dict = {}


class SyncResponseStatusEnum(Enum):
    rcvd = "rcvd"
    pdng = "pdng"
    succ = "succ"
    rjct = "rjct"


class SyncRequest(BaseModel):
    signature: str
    header: SyncRequestHeader
    message: dict


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
    version: str = "1.0.0"
    message_id: str
    message_ts: str
    action: str
    status: SyncResponseStatusEnum
    status_reason_code: SyncResponseStatusReasonCodeEnum
    status_reason_message: str
    total_count: int
    completed_count: int
    sender_id: str
    receiver_id: str
    is_msg_encrypted: bool = Field(
        validation_alias=AliasChoices("is_msg_encrypted", "is_encrypted"), default=False
    )
    meta: dict = {}


class SyncResponse(BaseModel):
    signature: str
    header: SyncResponseHeader
    message: dict
