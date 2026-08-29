from aiohttp import web
from sqlalchemy import Integer, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[int] = mapped_column(Integer)


engine = create_async_engine("sqlite+aiosqlite:///accounts.db")
Session = async_sessionmaker(engine, expire_on_commit=False)


async def transfer(request):
    data = await request.json()

    from_id = data["from_id"]
    to_id = data["to_id"]
    amount = data["amount"]

    async with Session() as session:
        try:
            async with session.begin():
                result_from = await session.execute(
                    select(Account).where(Account.id == from_id)
                )
                from_account = result_from.scalar_one_or_none()

                result_to = await session.execute(
                    select(Account).where(Account.id == to_id)
                )
                to_account = result_to.scalar_one_or_none()

                if from_account is None or to_account is None:
                    raise ValueError("Nie znaleziono konta")

                if from_account.balance < amount:
                    raise ValueError("Brak wystarczających środków")

                from_account.balance -= amount
                to_account.balance += amount

        except ValueError as error:
            raise web.HTTPBadRequest(text=str(error))

    return web.json_response(
        {
            "from_id": from_account.id,
            "from_balance": from_account.balance,
            "to_id": to_account.id,
            "to_balance": to_account.balance,
        }
    )


async def init_db(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as session:
        result = await session.execute(select(Account))
        accounts = result.scalars().all()

        if not accounts:
            session.add_all(
                [
                    Account(id=1, balance=1000),
                    Account(id=2, balance=500),
                ]
            )
            await session.commit()


app = web.Application()
app.on_startup.append(init_db)

app.router.add_post("/transfer", transfer)

web.run_app(app)
