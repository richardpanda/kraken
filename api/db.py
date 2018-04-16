import env

from config import Config, TestConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

config = TestConfig if env.is_testing else Config
engine = create_engine(config.DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)


def clear_db():
    import models
    Base.metadata.drop_all(bind=engine)
