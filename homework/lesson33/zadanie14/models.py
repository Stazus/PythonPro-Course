from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    price: Mapped[float] = mapped_column(Float)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id")
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
