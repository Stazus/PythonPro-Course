from aiohttp import web
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)


engine = create_engine("sqlite:///products.db")

Base.metadata.create_all(engine)


async def get_products(request):
    with Session(engine) as session:
        products = session.scalars(select(Product)).all()

        response_data = [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
            for product in products
        ]

    return web.json_response(response_data)


app = web.Application()
app.router.add_get("/products", get_products)

web.run_app(app)
