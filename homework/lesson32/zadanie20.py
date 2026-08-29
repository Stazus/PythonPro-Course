from aiohttp import web
from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class Product(Base):
    __tablename__ = "products_join"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship()


engine = create_async_engine("sqlite+aiosqlite:///join.db")
Session = async_sessionmaker(engine, expire_on_commit=False)


async def get_product(request):
    product_id = int(request.match_info["id"])

    async with Session() as session:
        result = await session.execute(
            select(Product, User)
            .join(User)
            .where(Product.id == product_id)
        )

        row = result.first()

        if row is None:
            raise web.HTTPNotFound()

        product, user = row

    return web.json_response(
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "creator": user.name,
        }
    )


async def init_db(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

        if not users:
            user = User(id=1, name="Stanisław")
            product = Product(
                id=1,
                name="Klawiatura",
                price=12999,
                user_id=1,
            )

            session.add_all([user, product])
            await session.commit()


app = web.Application()
app.on_startup.append(init_db)

app.router.add_get("/products/{id}", get_product)

web.run_app(app)
