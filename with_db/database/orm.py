from typing import Generic, List, Type, TypeVar, Dict
from sqlalchemy import  select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from database.database import Base
from funcs import check_fast_start_bonus

import logging

from .models import User, Package, Purchase

T = TypeVar("T", bound=Base)


class CRUD(Generic[T]):
    def __init__(self, model: Type[T], session_factory: sessionmaker):
        self.model = model
        self.session_factory = session_factory

    def create(self, **kwargs) -> T:
        with self.session_factory() as session:
            obj = self.model(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get(self, id: int) -> T | None:
        with self.session_factory() as session:
            query = select(self.model).filter_by(id=id)
            result = session.execute(query)
            try:
                return result.scalars().one()
            except NoResultFound:
                return None

    def get_all(self, **kwargs) -> List[T]:
        with self.session_factory() as session:
            query = select(self.model).filter_by(**kwargs).order_by(self.model.id.desc())
            result = session.execute(query)
            users = result.scalars().all()
            return users

    def update(self, id: int, **kwargs) -> T | None:
        with self.session_factory() as session:
            query = select(self.model).filter_by(id=id)
            result = session.execute(query)
            try:
                obj = result.scalars().one()
                for key, value in kwargs.items():
                    setattr(obj, key, value)

                session.commit()
                session.refresh(obj)
                return obj
            except NoResultFound:
                return None

    def delete(self, id: int) -> bool:
        with self.session_factory() as session:
            query = select(self.model).filter_by(id=id)
            result = session.execute(query)
            try:
                obj = result.scalars().one()
                session.delete(obj)
                session.commit()
                return True
            except NoResultFound:
                return False


class UsersRepo(CRUD[User]):
    def __init__(self, session):
        super().__init__(User, session)
        
    def check_all_users_bonus(self) -> Dict[int, List[int]]:
        with self.session_factory() as session:
            users = session.execute(select(User)).scalars().all()

            return check_fast_start_bonus(users)


class SyncORM:
    session_factory: sessionmaker

    # models
    users: UsersRepo
    packages: CRUD[Package]
    purchases: CRUD[Purchase]

    @classmethod
    def set_session_factory(cls, session_factory):
        cls.session_factory = session_factory

    @classmethod
    def init_models(cls):
        cls.users = UsersRepo(cls.session_factory)
        cls.packages = CRUD(Package, cls.session_factory)
        cls.purchases = CRUD(Purchase, cls.session_factory)

    @classmethod
    def create_tables(cls, engine):
        Base.metadata.create_all(engine)
            

    @classmethod
    def create_sample_data(cls):
        package_500 = cls.packages.create(name=500)
        package_1500 = cls.packages.create(name=1500)
        package_3000 = cls.packages.create(name=3000)

        user1 = cls.users.create(referal_id=None)
        user2 = cls.users.create(referal_id=user1.id)
        user3 = cls.users.create(referal_id=user1.id)
        user4 = cls.users.create(referal_id=user2.id)
        user5 = cls.users.create(referal_id=user2.id)
        user6 = cls.users.create(referal_id=user3.id)
        user7 = cls.users.create(referal_id=user3.id)

        cls.purchases.create(user_id=user2.id, package_id=package_1500.id)
        cls.purchases.create(user_id=user3.id, package_id=package_1500.id)
        cls.purchases.create(user_id=user4.id, package_id=package_3000.id)
        cls.purchases.create(user_id=user5.id, package_id=package_1500.id)
        cls.purchases.create(user_id=user6.id, package_id=package_1500.id)
        cls.purchases.create(user_id=user7.id, package_id=package_1500.id)

        logging.info("Sample data created successfully.")