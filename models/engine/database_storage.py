#!/usr/bin/python3
"""
Contains the DataBase_Storage  --- MYSQL ---
"""
from os import getenv
from sqlalchemy.exc import NoResultFound, InvalidRequestError
import models
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        UL_USER = getenv('UL_USER')
        UL_PWD = getenv('UL_PWD')
        UL_HOST = getenv('UL_HOST')
        UL_DB = getenv('UL_DB')
        UL_ENV = getenv('UL_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(UL_USER,
                                             UL_PWD,
                                             UL_HOST,
                                             UL_DB))
        if UL_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    """
        - For User Object only!!! 
        """

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user in the database."""
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **filters) -> User:
        """Find a user in the database based on filters."""
        filter_fields, filter_values = [], []
        for field, value in filters.items():
            if hasattr(User, field):
                filter_fields.append(getattr(User, field))
                filter_values.append(value)
            else:
                raise InvalidRequestError(f"Invalid filter: {field}")
        user = self._session.query(User).filter(
            tuple_(*filter_fields).in_([tuple(filter_values)])
        ).first()
        if user is None:
            raise NoResultFound("User not found.")
        return user

    def update_user(self, user_id: int, **updates) -> None:
        """Update user information in the database."""
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_fields = {}
        for key, value in updates.items():
            if hasattr(User, key):
                update_fields[getattr(User, key)] = value
            else:
                raise ValueError(f"Invalid field: {key}")
        self._session.query(User).filter(User.id == user_id).update(
            update_fields,
            synchronize_session=False,
        )
        self._session.commit()
