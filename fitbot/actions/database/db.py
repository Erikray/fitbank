import os
from types import TracebackType
from typing import Optional, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from dotenv import load_dotenv

load_dotenv()

class DBContextManager:
    def __init__(self, commit_on_exit: bool = False):
        self.commit_on_exit = commit_on_exit

        engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.active_session: Session = None

    def __enter__(self) -> Session:
        self.active_session = self.Session()
        return self.active_session

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if exc_type is not None:
            self.active_session.rollback()

        if self.commit_on_exit:
            self.active_session.commit()

        self.active_session.close()
