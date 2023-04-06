from fastapi import FastAPI

from account_book import models
from account_book.db import engine
from account_book.routes import account, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(account.router, prefix="/account-histories")
