from datetime import datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"


http_bearer = HTTPBearer()


def get_jwt_token(email: str, expired_at: datetime) -> str:
    return jwt.encode(
        {"sub": email, "exp": expired_at}, SECRET_KEY, algorithm=ALGORITHM
    )


async def check_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
