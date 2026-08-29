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


async def get_products(request):
    page = int(request.query.get("page", 1))
    limit = int(request.query.get("limit", 10))

    offset = (page - 1) * limit

    async with Session() as session:
        result = await session.execute(
            select(Product)
            .offset(offset)
            .limit(limit)
        )
        products = result.scalars().all()

    return web.json_response(
        [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
            for product in products
        ]
    )


async def init_db(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = web.Application()
app.on_startup.append(init_db)

app.router.add_get("/products", get_products)

web.run_app(app)
