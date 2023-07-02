from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExchangeRate(Base):
    __tablename__ = 'exchange_rate'

    id = Column(Integer, primary_key=True)
    currency = Column(String(3), nullable=False)
    date = Column(Date, nullable=False)
    rate = Column(Float, nullable=False)
