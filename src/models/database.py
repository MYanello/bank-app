from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
