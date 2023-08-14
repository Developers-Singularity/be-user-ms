import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from src.database import Base, db_session
from sqlalchemy.orm import sessionmaker, Session
from src.main import create_app
from src.extensions import SecurityManager, env_values
from src.models.user_model import User

engine = create_engine(env_values["DB_TEST_URI"], pool_size=0, max_overflow=-1)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session() -> Session:
    """Pytest session fixture to create a new database and drop it after test.

    :yield: session: database session
    :rtype: Iterator[Session]
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(session) -> TestClient:
    """Pytest client fixture to test FastAPI endpoints.
    :param session: Session to override default db_session
    :type session: Session
    :return: TestClient to send requests to FastAPI endpoints
    :rtype: TestClient
    """

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app = create_app()

    app.dependency_overrides[db_session] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="function")
def client_offline_db(session) -> TestClient:
    """Pytest client fixture to test FastAPI endpoints.
    :param session: Session to override default db_session
    :type session: Session
    :return: TestClient to send requests to FastAPI endpoints
    :rtype: TestClient
    """
    engine = create_engine("postgresql://username:password@localhost:3000/nonexist", pool_size=0, max_overflow=-1)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app = create_app()

    app.dependency_overrides[db_session] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="function")
def create_users(session):
    session.add(User(username="test_user_1", password=SecurityManager.hash(hash_string="test_user_pw_1")))
    session.add(User(username="test_user_2", password=SecurityManager.hash(hash_string="test_user_pw_2")))
    session.add(User(username="test_user_3", password=SecurityManager.hash(hash_string="test_user_pw_3")))
    session.commit()