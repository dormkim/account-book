from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, String, Table, create_engine)

TEST_DB_URL = "sqlite:///test_db.sqlite"


class DataBaseTable:
    def __init__(self):
        self.engine = create_engine(TEST_DB_URL)
        self.metadata = MetaData()

        self.users = Table(
            "users",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("email", String, unique=True),
            Column("password", String),
            Column("nickname", String, nullable=True),
            Column("is_active", Boolean),
        )

        self.account_histories = Table(
            "account_histories",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("amount", Integer),
            Column("memo", String, nullable=True),
            Column("is_deleted", Boolean),
            Column("is_withdrawn", Boolean),
            Column("user_id", Integer, ForeignKey("users.id")),
        )

        self.tokens = Table(
            "tokens",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("token", String),
            Column("expired_at", DateTime),
            Column("user_id", Integer, ForeignKey("users.id")),
        )

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def clear_tables(self):
        self.metadata.drop_all(self.engine)
