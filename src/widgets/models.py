import datetime as dt
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Widget(Base):

    __tablename__ = "widget"

    name = Column(String, primary_key=True)
    number_of_parts = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(
        self,
        name: str,
        number_of_parts: int,
        created_date: Optional[dt.datetime] = None,
        updated_date: Optional[dt.datetime] = None,
    ):
        self.name = name
        self.number_of_parts = number_of_parts
        self.created_date = (
            created_date if created_date is not None else dt.datetime.now()
        )
        self.updated_date = (
            updated_date if updated_date is not None else dt.datetime.now()
        )
