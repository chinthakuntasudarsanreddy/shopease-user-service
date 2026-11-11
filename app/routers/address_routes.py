
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user

from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)

from app.services.address_service import (
    create_address,
    list_addresses,
    get_address,
    update_address,
    delete_address,
    make_address_default,
)

router = APIRouter(
    prefix="/api/users/addresses",
    tags=["Addresses"],
)


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return create_address(
        db,
        current_user["auth_user_id"],
        address_data,
    )


@router.get(
    "",
    response_model=List[AddressResponse],
)
def get_addresses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return list_addresses(
        db,
        current_user["auth_user_id"],
    )


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
)
def get_single_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return get_address(
        db,
        current_user["auth_user_id"],
        address_id,
    )


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def edit_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return update_address(
        db,
        current_user["auth_user_id"],
        address_id,
        address_data,
    )


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return delete_address(
        db,
        current_user["auth_user_id"],
        address_id,
    )


@router.patch(
    "/{address_id}/default",
    response_model=AddressResponse,
)
def select_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return make_address_default(
        db,
        current_user["auth_user_id"],
        address_id,
    )
