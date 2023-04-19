from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine

from core.config import DATABASE_URL

metadata = MetaData()
engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)


def init_db():
    metadata.create_all(engine)
