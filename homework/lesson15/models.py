import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


zadania_tagi = Table(
    "zadania_tagi",
    Base.metadata,
    Column("id_zadania", Integer, ForeignKey("zadania.id"), primary_key=True),
    Column("id_tagu", Integer, ForeignKey("tagi.id"), primary_key=True),
)


class Zadanie(Base):
    __tablename__ = "zadania"

    id = Column(Integer, primary_key=True)
    opis = Column(String, nullable=False)
    zrobione = Column(Boolean, default=False, nullable=False)
    data_utworzenia = Column(DateTime, default=datetime.datetime.utcnow)

    tagi = relationship(
        "Tag",
        secondary=zadania_tagi,
        back_populates="zadania"
    )


class Tag(Base):
    __tablename__ = "tagi"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String, nullable=False, unique=True)

    zadania = relationship(
        "Zadanie",
        secondary=zadania_tagi,
        back_populates="tagi"
    )