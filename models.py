from sqlalchemy import Column, String, Integer, Float

from database.database import base, session


class AdsModel(base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True)
    photo_url = Column(String(200))
    title = Column(String(120), nullable=False)
    city = Column(String(60), nullable=False)
    date = Column(String(10), nullable=False)
    beds = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    currency = Column(String(1))
    price = Column(Float())

    def save_to_db(self):
        session.add(self)
        session.commit()
