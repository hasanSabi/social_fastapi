from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.auth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:newpassword@localhost:5432/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def setup_user2(test_client):
    user_data = {"email": "test2@example.com", "password": "password"}
    response = test_client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def setup_user(test_client):
    user_data = {"email": "test@example.com", "password": "password"}
    response = test_client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(setup_user):
    return create_access_token({"user_id": setup_user["id"]})

@pytest.fixture
def authorized_client(test_client, token):
    test_client.headers = {
        **test_client.headers,
        "Authorization": f"Bearer {token}"
    }
    return test_client


@pytest.fixture
def test_posts(setup_user, setup_user2, db_session):
    posts_data = [
        {"title": "First Post", "content": "Content of first post", "owner_id": setup_user["id"]},
        {"title": "Second Post", "content": "Content of second post", "owner_id": setup_user["id"]},
        {"title": "Third Post", "content": "Content of third post", "owner_id": setup_user["id"]},
        {"title": "Fourth Post", "content": "Content of fourth post", "owner_id": setup_user2["id"]}
    ]
    def create_post_model(post):
        return models.Post(**post)
    post_models = list(map(create_post_model, posts_data))
    db_session.add_all(post_models)
    db_session.commit()
    posts = db_session.query(models.Post).all()
    return posts
