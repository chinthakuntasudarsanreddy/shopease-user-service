
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schema import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfilePatch,
)


def create_user_profile(
    db: Session,
    auth_user_id: int,
    profile_data: UserProfileCreate,
):
    existing_user = (
        db.query(User)
        .filter(User.auth_user_id == auth_user_id)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User profile already exists",
        )

    new_user = User(
        auth_user_id=auth_user_id,
        **profile_data.model_dump(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_profile(db: Session, auth_user_id: int):
    user = (
        db.query(User)
        .filter(User.auth_user_id == auth_user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )

    return user


def update_user_profile(
    db: Session,
    auth_user_id: int,
    profile_data: UserProfileUpdate,
):
    user = get_user_profile(db, auth_user_id)

    for field, value in profile_data.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def patch_user_profile(
    db: Session,
    auth_user_id: int,
    profile_data: UserProfilePatch,
):
    user = get_user_profile(db, auth_user_id)

    update_data = profile_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided",
        )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user_profile(db: Session, auth_user_id: int):
    user = get_user_profile(db, auth_user_id)

    db.delete(user)
    db.commit()

    return {
        "message": "User profile deleted successfully. "
                   "Authentication account remains unchanged."
    }
