from sqlmodel import SQLModel, create_engine, Session

sqlite_file = "/var/lib/fireguard/fireguard.db"
engine = create_engine(f"sqlite:///{sqlite_file}")

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)