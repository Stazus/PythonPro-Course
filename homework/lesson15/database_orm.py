from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Zadanie, Tag

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
        return (
            db.query(Zadanie)
            .options(joinedload(Zadanie.tagi))
            .all()
        )

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
        
def dodaj_tag_do_zadania(id_zadania: int, nazwa_tagu: str):
    """Dodaje tag do zadania."""

    db = SessionLocal()

    try:
        zadanie = db.query(Zadanie).filter(
            Zadanie.id == id_zadania
        ).first()

        if not zadanie:
            return False

        tag = db.query(Tag).filter(
            Tag.nazwa == nazwa_tagu
        ).first()

        if not tag:
            tag = Tag(nazwa=nazwa_tagu)
            db.add(tag)

        zadanie.tagi.append(tag)
        db.commit()

        return True

    finally:
        db.close()