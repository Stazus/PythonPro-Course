from aiohttp import web
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)


engine = create_async_engine("sqlite+aiosqlite:///products.db")

Session = async_sessionmaker(engine, expire_on_commit=False)


async def get_product(request):
    product_id = int(request.match_info["id"])

    async with Session() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()

    if product is None:
        raise web.HTTPNotFound()

    return web.json_response(
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
    )


async def init_db(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = web.Application()
app.on_startup.append(init_db)

app.router.add_get("/products/{id}", get_product)

web.run_app(app)
