#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Returns first matching row in `users` for input param """
        for key, value in kwargs.items():
            if hasattr(User, key):
                pass
            else:
                raise InvalidRequestError()
        try:
            result = self._session.query(User).filter_by(**kwargs).one()
            if not result:
                raise NoResultFound()
            return result
        except NoResultFound:
            raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user with `user_id`"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not (hasattr(User, key)):
                raise ValueError()
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()
