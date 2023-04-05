import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

engine = create_engine(os.getenv("DB_URL"))


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
