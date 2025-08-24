import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker


def get_engine(db_path: str | None = None):
    if db_path is None:
        db_path = os.getenv("DB_PATH", "sqlite:///database.db")
    connect_args = (
        {"check_same_thread": False} if db_path.startswith("sqlite") else {}
    )
    return create_engine(db_path, connect_args=connect_args)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def add_and_commit(session: Session, instance) -> object:
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance
