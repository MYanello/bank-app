from datetime import UTC, datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Order(Base):
    """Model holding order information."""

    __tablename__ = "order"

    # TODO: add user_id foreign key once user auth is implemented
    id: Mapped[int | None] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    submitted: Mapped[datetime] = mapped_column(DateTime, index=True)
    term: Mapped[int] = mapped_column(Integer, index=True)
    amount: Mapped[int] = mapped_column(Integer, index=True)

    @property
    def submitted_iso(self) -> str:
        """Return the datetime in ISO8601 format with 'Z' suffix for UTC.

        Needed because sqlite does not store timezone info.
        """
        dt = self.submitted
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


class OrderCreate(BaseModel):
    """Create a new order."""

    term: int
    amount: int


class OrderResponse(BaseModel):
    """Response model for an order."""

    submitted: str
    term: int
    amount: int


class OrdersResponse(BaseModel):
    """Response model for list of orders."""

    orders: list[OrderResponse]
