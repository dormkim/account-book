from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from account_book.db import get_session
from account_book.models import (
    AccountHistoryRequest,
    AccountHistory,
    AccountHistoryResponse,
)
from account_book.utils.auth import check_jwt_token
from account_book.utils.user import get_user_id

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountHistoryResponse,
    tags=["account"],
)
async def post_account_hisotry(
    request: AccountHistoryRequest,
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history = AccountHistory()
    account_history.amount = request.amount
    account_history.memo = request.memo
    account_history.is_deleted = False
    account_history.is_withdrawn = request.is_withdrawn
    account_history.user_id = user_id

    db_session.add(account_history)
    db_session.commit()

    return {
        "id": account_history.id,
        "amount": account_history.amount,
        "memo": account_history.memo,
        "is_withdrawn": account_history.is_withdrawn,
    }


@router.post(
    "/recovery",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountHistoryResponse,
    tags=["account"],
)
async def recovery_account_history(
    history_id: int,
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history = (
        db_session.query(AccountHistory)
        .filter_by(user_id=user_id, id=history_id, is_deleted=False)
        .first()
    )
    account_history.is_deleted = False
    db_session.commit()

    return {
        "id": account_history.id,
        "amount": account_history.amount,
        "memo": account_history.memo,
        "is_withdrawn": account_history.is_withdrawn,
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[AccountHistoryResponse],
    tags=["account"],
)
async def get_account_hisotory_list(
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history_list = (
        db_session.query(AccountHistory)
        .filter_by(user_id=user_id, is_deleted=False)
        .all()
    )

    return account_history_list


@router.get(
    "/{history_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountHistoryResponse,
    tags=["account"],
)
async def get_account_hisotory(
    history_id: int,
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history = (
        db_session.query(AccountHistory)
        .filter_by(user_id=user_id, id=history_id, is_deleted=False)
        .first()
    )

    return account_history


@router.put(
    "/{history_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountHistoryResponse,
    tags=["account"],
)
async def put_account_hisotory(
    request: AccountHistoryRequest,
    history_id: int,
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history = (
        db_session.query(AccountHistory)
        .filter_by(user_id=user_id, id=history_id, is_deleted=False)
        .first()
    )

    if account_history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="History not found"
        )

    account_history.amount = request.amount
    account_history.memo = request.memo
    account_history.is_withdrawn = request.is_withdrawn

    db_session.commit()

    return account_history


@router.delete(
    "/{history_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountHistoryResponse,
    tags=["account"],
)
async def delete_account_hisotory(
    history_id: int,
    jwt_payload: str = Depends(check_jwt_token),
    db_session: Session = Depends(get_session),
):
    user_id = await get_user_id(jwt_payload=jwt_payload, db_session=db_session)

    account_history = (
        db_session.query(AccountHistory)
        .filter_by(user_id=user_id, id=history_id, is_deleted=False)
        .first()
    )

    if account_history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="History not found"
        )

    account_history.is_deleted = True
    db_session.commit()

    return account_history
