import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):  # noqa: D101
    pass


def get_engine(db_path: str | None = None):
    if db_path is None:
        db_path = os.getenv("DB_PATH", "sqlite:///database.db")
    connect_args = (
        {"check_same_thread": False} if db_path.startswith("sqlite") else {}
    )
    return create_engine(db_path, connect_args=connect_args)


def get_session(engine=None) -> Generator[Session]:
    if engine is None:
        engine = get_engine()
    with Session(engine) as session:
        yield session


def init_db(engine=None):
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(engine)


def add_and_commit(session: Session, instance) -> object:
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance
