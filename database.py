from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine

from core.config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
metadata = MetaData()
engine = create_engine(DATABASE_URL)


def init_db():
    metadata.create_all(engine)
