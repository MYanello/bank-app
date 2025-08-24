import logging
import os
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Query, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.database import add_and_commit, get_session, init_db
from models.orders import Order, OrderCreate, OrderResponse, OrdersResponse
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


SessionDep = Annotated[Session, Depends(lambda: next(get_session()))]
app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
def health_check() -> str:
    logger.debug("health check endpoint was called")
    return "OK"


@app.get("/api/v1/orders", response_model=OrdersResponse)
def get_orders(session: SessionDep) -> OrdersResponse:
    logger.info("Fetching all orders from the database")
    orders = session.execute(select(Order)).scalars().all()
    return OrdersResponse(
        orders=[
            OrderResponse(
                submitted=order.submitted, term=order.term, amount=order.amount
            )
            for order in orders
        ]
    )


@app.post("/api/v1/order", status_code=status.HTTP_202_ACCEPTED)
async def create_order(order: OrderCreate, session: SessionDep) -> Response:
    logger.info(
        "Order for term: %d and amount: %d received", order.term, order.amount
    )
    new_order = Order(
        term=order.term, amount=order.amount, submitted=datetime.now(UTC)
    )
    add_and_commit(session, new_order)
    logger.debug(
        "Successfully saved order for %d months of %d", order.term, order.amount
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.get("/api/v1/yields", response_model=dict[str, object])
def get_yields(
    year: int = Query(None, description="Year for yield data"),
    term: str = Query(None, description="Term length for yield data"),
) -> dict[str, object]:
    logger.info("Fetching yield data for %d, term: %s", year, term)
    return {"year": year, "term": term, "yields": fetch_yield_data(year, term)}


app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)


@app.get("/")
def read_index() -> FileResponse:
    parent_dir = os.path.dirname(__file__)
    file = os.path.join(parent_dir, "static", "index.html")
    return FileResponse(file)


@app.get("/orders")
def read_orders() -> FileResponse:
    parent_dir = os.path.dirname(__file__)
    file = os.path.join(parent_dir, "static", "orders.html")
    return FileResponse(file)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
