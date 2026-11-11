
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Address(Base):

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    # Reference to local user profile
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    address_type = Column(String(30), nullable=False)

    full_name = Column(String(150), nullable=False)

    phone_number = Column(String(20), nullable=False)

    address_line_1 = Column(String(255), nullable=False)

    address_line_2 = Column(String(255), nullable=True)

    city = Column(String(100), nullable=False)

    state = Column(String(100), nullable=False)

    country = Column(String(100), nullable=False)

    postal_code = Column(String(20), nullable=False)

    is_default = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relationship with User model
    user = relationship(
        "User",
        back_populates="addresses"
    )
