#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
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
        """
        A function that add new user to the database
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            # user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        A function that returns the first row found in
        the users table as filtered by the method’s input arguments.
        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError()
        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        A function that update the user
        will use find_user_by to locate the user to update.
        """
        try:
            values = {}
            user = self.find_user_by(id=user_id)
            if user is not None:
                for key, value in kwargs.items():
                    if hasattr(User, key):
                        values[key] = value
                    else:
                        raise ValueError()
                self._session.query(User).filter(User.id == user.id).update(
                    values,
                    synchronize_session=False
                )
                self._session.commit()
        except NoResultFound:
            raise
