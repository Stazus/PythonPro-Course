import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True)
    opis = Column(String, nullable=False)
    zrobione = Column(Boolean, default=False, nullable=False)
    data_utworzenia = Column(DateTime, default=datetime.datetime.utcnow)