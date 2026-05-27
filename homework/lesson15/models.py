from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True)
    opis = Column(String, nullable=False)
    zrobione = Column(Boolean, default=False)