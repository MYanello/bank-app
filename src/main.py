import logging
import os
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Query, Response, status
from sqlmodel import Session, select

from models.database import add_and_commit, get_session, init_db
from models.orders import Order, OrderCreate
from services import fetch_yield_data

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger("bank-app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
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
    logger.info("Fetching all orders from the database")
    return session.exec(select(Order)).all()


@app.post("/api/v1/order", status_code=status.HTTP_202_ACCEPTED)
async def create_order(order: OrderCreate, session: SessionDep):
    logger.info("Order for %d and amount %d received", order.term, order.amount)
    new_order = Order(
        term=order.term, amount=order.amount, submitted=datetime.now(UTC)
    )
    add_and_commit(session, new_order)
    logger.debug(
        "Successfully saved order for %d months of %d", order.term, order.amount
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.get("/api/v1/yields")
def get_yields(year: int = Query(None, description="Year for yield data")):
    logger.info("Fetching yield data for year: %s", year)
    return fetch_yield_data(year=year)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
