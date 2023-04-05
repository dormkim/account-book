from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from account_book.models import AuthToken, User


async def get_user_id(jwt_payload: dict, db_session: Session):
    user_email = jwt_payload["sub"]
    token_expired_at = jwt_payload["exp"]
    if token_expired_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token",
        )

    find_user = (
        db_session.query(User)
        .join(
            AuthToken,
            User.id == AuthToken.user_id,
        )
        .filter(User.email == user_email, User.is_active is True)
        .first()
    )
    if find_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User",
        )

    return find_user.id
