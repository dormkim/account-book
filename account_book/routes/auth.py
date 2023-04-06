from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from account_book.constants import EXPIRATION_TIME_MINUTES
from account_book.db import get_session
from account_book.models import (AuthToken, AuthTokenResponse, SignUpResponse,
                                 User, UserRequest)
from account_book.utils.auth import get_jwt_token

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=SignUpResponse,
    tags=["auth"],
)
async def signup(
    request: UserRequest,
    db_session: Session = Depends(get_session),
):
    find_user = db_session.query(User).filter_by(email=request.email).first()
    if find_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Registered email"
        )

    new_user = User(
        email=request.email,
        hashed_password=bcrypt.hashpw(
            request.password.encode("utf-8"), bcrypt.gensalt()
        ),
        nickname=request.nickname,
        is_active=True,
    )

    db_session.add(new_user)
    db_session.commit()

    return {
        "email": request.email,
    }


@router.post(
    "/signin",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthTokenResponse,
    tags=["auth"],
)
async def signin(
    request: UserRequest,
    db_session: Session = Depends(get_session),
):
    find_user = db_session.query(User).filter_by(email=request.email).first()
    if find_user is None or find_user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalied Email",
        )
    if not bcrypt.checkpw(
        request.password.encode(),
        find_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password",
        )

    user_token = (
        db_session.query(AuthToken)
        .filter_by(
            user_id=find_user.id,
        )
        .first()
    )

    expired_at = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_MINUTES)
    token = get_jwt_token(request.email, expired_at)

    if user_token:
        user_token.token = token
        user_token.expired_at = expired_at

    else:
        auth_token = AuthToken(
            token=token,
            expired_at=expired_at,
            user_id=find_user.id,
        )

        db_session.add(auth_token)

    db_session.commit()

    return {
        "email": find_user.email,
        "token": token,
        "expired_at": expired_at,
    }
