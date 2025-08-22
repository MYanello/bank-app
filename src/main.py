import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from sqlmodel import Session

from models.database import get_session
from services import fetch_yield_data

logging.basicConfig(
    level=logging.DEBUG,
)
logger = logging.getLogger("bank-app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    # db_init()
    yield
    # Shutdown logic


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
def health_check():
    logger.info("health check endpoint was called")
    return "OK"


@app.get("/api/v1/orders")
def get_orders(session: SessionDep):
    return {"message": "Orders retrieved successfully"}


@app.post("/api/v1/order")
def create_order(session: SessionDep):
    return {"message": "Order created successfully"}


@app.get("/api/v1/yields")
def get_yields(year: int = Query(None, description="Year for yield data")):
    logger.info("Fetching yield data for year: %s", year)
    return fetch_yield_data(year=year)
