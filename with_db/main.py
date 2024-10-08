from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.orm import SyncORM


def setup_db():
    engine = create_engine(
        "sqlite:///db.db",
        # echo=True
        )
    session_factory = sessionmaker(bind=engine)
    SyncORM.set_session_factory(session_factory)
    SyncORM.init_models()
    SyncORM.create_tables(engine)
    SyncORM.create_sample_data()


def main():
    setup_db()
    result = SyncORM.users.check_all_users_bonus()
    for user_id, refs in result.items():
        print(user_id, refs)


if __name__ == "__main__":
    main()