from aiohttp import web
from sqlalchemy import Integer, String, create_engine
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


async def create_product(request):
    data = await request.json()

    product = Product(
        name=data["name"],
        price=data["price"],
    )

    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)

        response_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }

    return web.json_response(response_data, status=201)


app = web.Application()
app.router.add_post("/products", create_product)

web.run_app(app)
