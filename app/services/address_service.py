
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.address_model import Address
from app.models.user_model import User
from app.schemas.address_schema import AddressCreate, AddressUpdate


def get_local_user(db: Session, auth_user_id: int):
    user = (
        db.query(User)
        .filter(User.auth_user_id == auth_user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Create your profile first.",
        )

    return user


def get_owned_address(
    db: Session,
    user_id: int,
    address_id: int,
):
    address = (
        db.query(Address)
        .filter(
            Address.id == address_id,
            Address.user_id == user_id,
        )
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    return address


def set_default_address(db: Session, user_id: int, address_id: int):
    # Lock this user's address rows while changing the default.
    addresses = (
        db.query(Address)
        .filter(Address.user_id == user_id)
        .with_for_update()
        .all()
    )

    selected = next(
        (address for address in addresses if address.id == address_id),
        None,
    )

    if selected is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    try:
        for address in addresses:
            address.is_default = address.id == address_id

        db.commit()
        db.refresh(selected)
        return selected
    except Exception:
        db.rollback()
        raise


def create_address(
    db: Session,
    auth_user_id: int,
    address_data: AddressCreate,
):
    user = get_local_user(db, auth_user_id)

    try:
        existing_count = (
            db.query(Address)
            .filter(Address.user_id == user.id)
            .count()
        )

        data = address_data.model_dump()

        # First address becomes default automatically.
        make_default = data.pop("is_default", False) or existing_count == 0

        if make_default:
            db.query(Address).filter(
                Address.user_id == user.id
            ).update(
                {Address.is_default: False},
                synchronize_session="fetch",
            )

        new_address = Address(
            user_id=user.id,
            **data,
            is_default=make_default,
        )

        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return new_address

    except Exception:
        db.rollback()
        raise


def list_addresses(db: Session, auth_user_id: int):
    user = get_local_user(db, auth_user_id)

    return (
        db.query(Address)
        .filter(Address.user_id == user.id)
        .order_by(Address.is_default.desc(), Address.id.desc())
        .all()
    )


def get_address(
    db: Session,
    auth_user_id: int,
    address_id: int,
):
    user = get_local_user(db, auth_user_id)
    return get_owned_address(db, user.id, address_id)


def update_address(
    db: Session,
    auth_user_id: int,
    address_id: int,
    address_data: AddressUpdate,
):
    user = get_local_user(db, auth_user_id)
    address = get_owned_address(db, user.id, address_id)

    data = address_data.model_dump()
    make_default = data.pop("is_default", False)

    try:
        if make_default:
            db.query(Address).filter(
                Address.user_id == user.id,
                Address.id != address.id,
            ).update(
                {Address.is_default: False},
                synchronize_session="fetch",
            )

        for field, value in data.items():
            setattr(address, field, value)

        address.is_default = make_default

        db.commit()
        db.refresh(address)
        return address

    except Exception:
        db.rollback()
        raise


def delete_address(
    db: Session,
    auth_user_id: int,
    address_id: int,
):
    user = get_local_user(db, auth_user_id)
    address = get_owned_address(db, user.id, address_id)

    try:
        db.delete(address)
        db.commit()

        return {"message": "Address deleted successfully"}

    except Exception:
        db.rollback()
        raise


def make_address_default(
    db: Session,
    auth_user_id: int,
    address_id: int,
):
    user = get_local_user(db, auth_user_id)

    return set_default_address(db, user.id, address_id)
