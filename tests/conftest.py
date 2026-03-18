import uuid
from datetime import datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.dependencies import get_current_user
from app.database.database import Base, get_db
from app.database.models import Calendar, User
from config import Settings
from main import app


@pytest.fixture
def test_db():
    # Note: SQLite in-memory is used for unit test speed and isolation.
    # Production runtime uses Supabase PostgreSQL configured in DATABASE_URL.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(test_db: Session):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_a(test_db: Session):
    calendar = Calendar(
        id=str(uuid.uuid4()),
        name="Household A",
    )
    test_db.add(calendar)
    test_db.commit()

    user = User(
        id=str(uuid.uuid4()),
        email="usera@example.com",
        name="User A",
        google_id="google_a",
        calendar_id=calendar.id,
        last_login=datetime.utcnow(),
    )
    calendar.owner_user_id = user.id
    test_db.add(user)
    test_db.add(calendar)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_user_b(test_db: Session):
    user = User(
        id=str(uuid.uuid4()),
        email="userb@example.com",
        name="User B",
        google_id="google_b",
        last_login=datetime.utcnow(),
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def authenticated_client(test_db: Session, test_user_a: User):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    async def override_get_current_user():
        return test_user_a

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    settings = Settings()
    token = jwt.encode(
        {
            "user_id": test_user_a.id,
            "email": test_user_a.email,
            "exp": datetime.utcnow() + timedelta(hours=1),
        },
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    client.cookies.set("session", token, domain="testserver", path="/")
    try:
        yield client
    finally:
        app.dependency_overrides.clear()
