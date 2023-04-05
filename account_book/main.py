from account_book.db import engine
from account_book import models
from fastapi import FastAPI

from account_book.routes import auth, account

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(account.router, prefix="/account_histories")
