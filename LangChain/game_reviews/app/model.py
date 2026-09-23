from sqlalchemy import (
    String,
    Integer,
    Float,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    # Temporary plain-text password.
    # Hashing/authentication can be added later.
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Useful for future authorization
    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False
    )

    # Useful for future authentication/authorization
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    reviews: Mapped[list["GameReview"]] = relationship(
        "GameReview",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class GameReview(Base):

    __tablename__ = "game_reviews"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    game_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    review: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="reviews"
    )