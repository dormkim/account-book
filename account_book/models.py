from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from account_book.db import Base


class UserRequest(BaseModel):
    email: str
    password: str
    nickname: Optional[str]


class SignUpResponse(BaseModel):
    email: str


class AuthTokenResponse(BaseModel):
    email: str
    token: str
    expired_at: datetime


class AccountHistoryRequest(BaseModel):
    amount: conint(ge=0)
    memo: Optional[str]
    is_withdrawn: bool


class AccountHistoryResponse(BaseModel):
    id: int
    amount: int
    memo: Optional[str]
    is_withdrawn: bool


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    nickname = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    histories = relationship("AccountHistory", backref="users")
    tokens = relationship("AuthToken", backref="users")

    def __init__(self, email, hashed_password, nickname, is_active):
        self.email = email
        self.hashed_password = hashed_password
        self.nickname = nickname
        self.is_active = is_active


class AccountHistory(Base):
    __tablename__ = "account_histories"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    memo = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=True)
    is_withdrawn = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, amount, memo, is_deleted, is_withdrawn, user_id):
        self.amount = amount
        self.memo = memo
        self.is_deleted = is_deleted
        self.is_withdrawn = is_withdrawn
        self.user_id = user_id


class AuthToken(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    expired_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    def __init__(self, token, expired_at, user_id):
        self.token = token
        self.expired_at = expired_at
        self.user_id = user_id
