
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user

from app.schemas.user_schema import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfilePatch,
    UserProfileResponse,
)

from app.services.user_service import (
    create_user_profile,
    get_user_profile,
    update_user_profile,
    patch_user_profile,
    delete_user_profile,
)

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.post(
    "/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return create_user_profile(
        db,
        current_user["auth_user_id"],
        profile_data,
    )


@router.get(
    "/profile",
    response_model=UserProfileResponse,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return get_user_profile(
        db,
        current_user["auth_user_id"],
    )


@router.put(
    "/profile",
    response_model=UserProfileResponse,
)
def update_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return update_user_profile(
        db,
        current_user["auth_user_id"],
        profile_data,
    )


@router.patch(
    "/profile",
    response_model=UserProfileResponse,
)
def patch_profile(
    profile_data: UserProfilePatch,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return patch_user_profile(
        db,
        current_user["auth_user_id"],
        profile_data,
    )


@router.delete("/profile")
def remove_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return delete_user_profile(
        db,
        current_user["auth_user_id"],
    )
