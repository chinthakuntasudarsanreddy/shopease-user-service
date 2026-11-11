
from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


# Common Address Fields
class AddressBase(BaseModel):

    address_type: str = Field(
        ...,
        min_length=2,
        max_length=30
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=20
    )

    address_line_1: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    address_line_2: Optional[str] = Field(
        default=None,
        max_length=255
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    state: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    country: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    postal_code: str = Field(
        ...,
        min_length=3,
        max_length=20
    )

    is_default: bool = False

    @field_validator("address_type")
    @classmethod
    def validate_address_type(cls, value):

        value = value.strip().title()

        if value not in ["Home", "Office", "Other"]:
            raise ValueError(
                "Address type must be Home, Office or Other"
            )

        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError("Recipient name is required")

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):

        value = value.strip()

        if not value.isdigit() or not 10 <= len(value) <= 20:
            raise ValueError("Invalid phone number")

        return value


# Create Address Request
class AddressCreate(AddressBase):
    pass


# Update Address Request
class AddressUpdate(AddressBase):
    pass


# Address Response
class AddressResponse(AddressBase):

    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
