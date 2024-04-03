from enum import Enum
from typing import Dict, List, Optional, Union
from datetime import datetime
from ...common.schemas.status_codes import StatusEnum
from pydantic import AliasChoices, BaseModel, Field, field_validator


class UpdateStatusReasonCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_beneficiary_name_invalid = "rjct.beneficiary_name.invalid"
    rjct_id_invalid = "rjct.id.invalid"

class AdditionalInfo(BaseModel):
    name: str = Field(validation_alias=AliasChoices("name", "key"))
    value: Union[int, float, str, bool, dict]

class SingleUpdateRequest(BaseModel):
    reference_id: str
    timestamp: datetime
    id: str
    fa: str
    name: Optional[str] = None
    phone_number: Optional[str] = None
    additional_info: Optional[List[AdditionalInfo]] = None
    locale: Optional[str] = "en"

    @field_validator("additional_info")
    @classmethod
    def convert_addl_info_dict_list(
        cls, v: Optional[Union[List[AdditionalInfo], AdditionalInfo]]
    ):
        if v and not isinstance(v, list):
            v = [v]
        return v
class UpdateRequest(BaseModel):
    transaction_id: str
    update_request: List[SingleUpdateRequest]


class SingleUpdateResponse(BaseModel):
    reference_id: str
    timestamp: datetime
    id: Optional[str] = ""
    status: StatusEnum
    status_reason_code: Optional[UpdateStatusReasonCode] = None
    status_reason_message: Optional[str] = ""
    additional_info: Optional[List[object]] = None
    locale: Optional[str] = "en"


class UpdateResponse(BaseModel):
    transaction_id: str
    correlation_id: Optional[str] = ""
    update_response: List[SingleUpdateResponse]
