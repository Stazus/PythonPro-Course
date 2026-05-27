from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Zadanie

DATABASE_URL = "sqlite:///todo_orm.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def dodaj_zadanie(opis: str):

    db = SessionLocal()

    try:
        zadanie = Zadanie(opis=opis)

        db.add(zadanie)

        db.commit()

    finally:
        db.close()


def pobierz_zadania():

    db = SessionLocal()

    try:
        return db.query(Zadanie).all()

    finally:
        db.close()


def oznacz_jako_zrobione(id_zadania: int):

    db = SessionLocal()

    try:
        zadanie = db.query(Zadanie).filter(
            Zadanie.id == id_zadania
        ).first()

        if zadanie:
            zadanie.zrobione = True

            db.commit()

    finally:
        db.close()


def usun_zadanie(id_zadania: int):

    db = SessionLocal()

    try:
        zadanie = db.query(Zadanie).filter(
            Zadanie.id == id_zadania
        ).first()

        if zadanie:
            db.delete(zadanie)

            db.commit()

    finally:
        db.close()
        
        
def wyszukaj_zadania(fraza: str):
    """Wyszukuje zadania po fragmencie opisu."""

    with SessionLocal() as db:

        return (
            db.query(Zadanie)
            .filter(Zadanie.opis.contains(fraza))
            .all()
        )