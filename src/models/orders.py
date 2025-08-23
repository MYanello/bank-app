from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
    """Model holding order information."""

    # TODO: add user_id foreign key once user auth is implemented
    id: int | None = Field(default=None, primary_key=True)
    submitted: datetime = Field(index=True)
    term: int = Field(index=True)
    amount: float = Field(index=True)


class OrderCreate(SQLModel):
    """Create a new order."""

    term: int
    amount: float = Field(index=True)


class OrderResponse(SQLModel):
    """Response model for an order."""

    submitted: datetime
    term: int
    amount: float

    @property
    def submitted_iso(self) -> str:
        """Return the datetime in ISO8601 format with 'Z' suffix for UTC.

        Needed because sqlite does not store timezone info.
        """
        dt = self.submitted
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")
