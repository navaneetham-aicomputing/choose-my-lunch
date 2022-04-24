from contextlib import contextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

_test_engine = create_async_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=_test_engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
