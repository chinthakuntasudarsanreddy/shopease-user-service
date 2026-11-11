
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class User(Base):

    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "auth_user_id",
            name="uq_users_auth_user_id"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    # ID received from Authentication Service
    auth_user_id = Column(Integer, nullable=False, index=True)

    full_name = Column(String(150), nullable=False)

    phone_number = Column(String(20), nullable=False)

    date_of_birth = Column(Date, nullable=True)

    gender = Column(String(20), nullable=True)

    profile_image = Column(String(500), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # One user can have multiple addresses
    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )
