import os
from unittest import mock

from fastapi.testclient import TestClient

from tests.table import TEST_DB_URL, DataBaseTable

TEST_ACCOUNT_HISTORY_ITEM = {
    "amount": 111,
    "memo": "test",
    "is_withdrwan": True,
}

TEST_USER_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    + "eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNjgwNjc0NDAwfQ"
    + ".7n7B5hXMb4lINOVoWw95VexjQLz4APaS7xGlw9dIr6w"
)
TEST_HEADER = {"Authorization": f"Bearer {TEST_USER_TOKEN}"}


@mock.patch.dict(os.environ, {"DB_URL": TEST_DB_URL}, clear=True)
class TestAccountHistory:
    def setUp(self) -> None:
        db_table = DataBaseTable()
        db_table.clear_tables()
        db_table.create_tables()

    def test_post_account_history(self):
        from account_book.main import app

        with TestClient(app) as client:
            client.headers.update(TEST_HEADER)

            response = client.post(
                "/account-histories",
                json=TEST_ACCOUNT_HISTORY_ITEM,
            )

            assert response.status_code == 201
            assert response.json()["amount"] == 111
            assert response.json()["memo"] == "test"
            assert response.json()["is_withdrwan"] is True
