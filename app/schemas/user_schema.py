
from datetime import date, datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


# Common User Profile Fields
class UserProfileBase(BaseModel):

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

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    profile_image: Optional[str] = Field(
        default=None,
        max_length=500
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError("Full name cannot be empty")

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits"
            )

        if len(value) < 10 or len(value) > 20:
            raise ValueError(
                "Phone number must contain 10 to 20 digits"
            )

        return value

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value):

        if value is not None:
            value = value.strip()

            if value.lower() not in [
                "male",
                "female",
                "other"
            ]:
                raise ValueError(
                    "Gender must be Male, Female or Other"
                )

        return value


# Create Profile Request
class UserProfileCreate(UserProfileBase):
    pass


# Update Profile Request
class UserProfileUpdate(UserProfileBase):
    pass


# Partial Update Profile Request
class UserProfilePatch(BaseModel):

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    phone_number: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=20
    )

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    profile_image: Optional[str] = Field(
        default=None,
        max_length=500
    )

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):

        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError(
                    "Full name cannot be empty"
                )

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):

        if value is not None:

            value = value.strip()

            if not value.isdigit() or not 10 <= len(value) <= 20:
                raise ValueError(
                    "Invalid phone number"
                )

        return value


# Profile Response
class UserProfileResponse(UserProfileBase):

    id: int
    auth_user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
