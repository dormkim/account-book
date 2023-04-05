from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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


class AccountHistory(Base):
    __tablename__ = "accounthistories"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    memo = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=True)
    is_withdrawn = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class AuthToken(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    expired_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
