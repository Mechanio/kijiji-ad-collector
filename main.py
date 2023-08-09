from database.database import db

from parser import parser
from models import AdsModel


def create_db():
    AdsModel.__table__.create(bind=db, checkfirst=True)


if __name__ == "__main__":
    create_db()
    # get_data_with_selenium("https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273")
    parser()
