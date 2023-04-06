import os
from datetime import datetime
from unittest import mock

from fastapi.testclient import TestClient

from tests.table import TEST_DB_URL, DataBaseTable

TEST_SIGNUP_REQUEST = {
    "email": "test@example.com",
    "password": "test1234",
    "nickname": "test_user",
}

TEST_SIGNIN_REQUEST = {
    "email": "test@example.com",
    "password": "test1234",
}
TEST_USER_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    + "eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjgwNjc0NDAwfQ"
    + ".7n7B5hXMb4lINOVoWw95VexjQLz4APaS7xGlw9dIr6w"
)


@mock.patch.dict(os.environ, {"DB_URL": TEST_DB_URL}, clear=True)
class TestAuth:
    def setUp(self) -> None:
        db_table = DataBaseTable()
        db_table.clear_tables()
        db_table.create_tables()

    def test_success_signup(self):
        from account_book.main import app

        with TestClient(app) as client:
            response = client.post("/signup", json=TEST_SIGNUP_REQUEST)

            assert response.status_code == 201
            assert response.json()["email"] == "test@example.com"

    def test_duplicate_signup(self):
        from account_book.main import app

        with TestClient(app) as client:
            response = client.post("/signup", json=TEST_SIGNUP_REQUEST)

            assert response.status_code == 201

            response = client.post("/signup", json=TEST_SIGNUP_REQUEST)

            assert response.status_code == 409

    @mock.patch("account_book.routes.auth.datetime")
    def test_success_signin(self, mock_dt):
        from account_book.main import app

        mock_dt.utcnow = mock.Mock(return_value=datetime(2023, 4, 5, 0, 0, 0))
        with TestClient(app) as client:
            response = client.post("/signin", json=TEST_SIGNIN_REQUEST)

            assert response.status_code == 201
            assert response.json()["email"] == "test@example.com"
            assert response.json()["token"] == TEST_USER_TOKEN
            assert response.json()["expired_at"] == datetime(
                2023, 4, 5, 6, 0, 0
            ).strftime("%Y-%m-%dT%H:%M:%S")

    def test_not_exist_user_signin(self):
        from account_book.main import app

        with TestClient(app) as client:
            invalid_user = TEST_SIGNIN_REQUEST.copy()
            invalid_user["email"] = "invalid@test.com"

            response = client.post("/signin", json=invalid_user)

            assert response.status_code == 401

    def test_password_is_not_correct(self):
        from account_book.main import app

        with TestClient(app) as client:
            invalid_user = TEST_SIGNIN_REQUEST.copy()
            invalid_user["password"] = "1234"

            response = client.post("/signin", json=invalid_user)

            assert response.status_code == 401
