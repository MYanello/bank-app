from datetime import date

from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
    """Model holding order information."""

    # TODO: add user_id foreign key once user auth is implemented
    id: int | None = Field(default=None, primary_key=True)
    submitted: date = Field(index=True)
    term: int = Field(index=True)
    amount: float = Field(index=True)


class OrderCreate(SQLModel):
    """Create a new order."""

    term: int
    amount: float = Field(index=True)
