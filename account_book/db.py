import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

engine = create_engine(os.getenv("DB_URL"))
Base = declarative_base()


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
