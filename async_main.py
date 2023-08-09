from database.database import db

from async_parser import async_parser
from models import AdsModel


def create_db():
    AdsModel.__table__.create(bind=db, checkfirst=True)


if __name__ == "__main__":
    create_db()
    async_parser()
