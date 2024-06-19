import enum


class DomainEnum(enum.Enum):
    AUTH = "AUTH"


class SecurityErrorCodes(enum.Enum):
    INVALID_JWT_SIGNATURE = "INVALID JWT SIGNATURE"
