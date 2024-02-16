import threading
import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import context


logger = logging.getLogger('dao.postgres_dao')

_the_sessionmaker = None
_engine = None


def get_engine():
    global _engine

    if _engine is None:
        with threading.Lock():
            if _engine is None:
                _engine = create_engine(
                    context.DB_URL,
                    echo=context.DB_SQLALCHEMY_ECHO,
                    pool_pre_ping=True)
    return _engine


def get_session():
    global _the_sessionmaker
    if _the_sessionmaker is None:
        with threading.Lock():
            if _the_sessionmaker is None:
                get_engine()
                _the_sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=_engine, future=True)
    return _the_sessionmaker()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
