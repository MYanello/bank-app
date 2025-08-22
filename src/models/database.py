from sqlmodel import Session, create_engine

# def db_init():
#     """Set up the sqlite db and create tables."""
#     sqlite_file_name = os.getenv("SQLITE_FILE_NAME", "database.db")
#     sqlite_url = f"sqlite:///{sqlite_file_name}"
#     connect_args = {"check_same_thread": False}
#     engine = create_engine(sqlite_url, connect_args=connect_args)
#     SQLModel.metadata.create_all(engine)
#     get_session(engine)


# def get_session(engine):
#     with Session(engine) as session:
#         yield session

# models/database.py

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session
