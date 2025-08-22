from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from models.database import get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    # db_init()
    yield
    # Shutdown logic


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/orders")
def get_orders(session: SessionDep):
    return {"message": "Orders retrieved successfully"}


@app.post("/api/v1/order")
def create_order(session: SessionDep):
    return {"message": "Order created successfully"}


@app.get("/api/v1/yields")
def get_yields(session: SessionDep):
    return {"message": "Yields retrieved successfully"}
