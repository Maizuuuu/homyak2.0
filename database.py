from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

BaseModel: DeclarativeBase = declarative_base()

engine = create_engine(
    "sqlite:///data.sqlite", connect_args={"check_same_thread": False, "timeout": 30}
)
create_session = sessionmaker(bind=engine, expire_on_commit=False, autocommit=False)


def create_all_table():
    BaseModel.metadata.create_all(bind=engine)
