from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_create_user(test_client):
    response = test_client.post("/users/", json={"email": "test1@example.com", "password": "password"})
    new_user = schemas.UserOut(**response.json())

    # Accept either created or already exists
    assert response.status_code == 201 or response.status_code == 400 
    if response.status_code == 201:
        assert new_user.email == "test1@example.com"
    if response.status_code == 400:
        assert response.json().get("detail") == "Email already registered"


def test_login_user(test_client, setup_user):

    response = test_client.post("/login", data={"username": setup_user["email"], "password": setup_user["password"]})

   # print(response.json())

    assert response.status_code == 200
    token = schemas.Token(**response.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert token.token_type == "bearer"
    assert id == setup_user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("test@example.com", "wrongpassword", 403),
    ("nonexistent@example.com", "wrongpassword", 403)
])
def test_incorrect_login(test_client, email, password, status_code, setup_user):
    response = test_client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
