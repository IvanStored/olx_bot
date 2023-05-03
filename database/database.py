from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from settings import Config

engine = create_engine(url=Config.SQLALCHEMY_DATABASE_URI, echo=True)
db_session = scoped_session(
    session_factory=sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
)
Base = declarative_base()
