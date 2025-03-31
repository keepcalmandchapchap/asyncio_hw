import os
import asyncio
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, String

POSTGRES_DB = os.getenv("POSTGRES_DB", "star_wars")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Persons(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String)
    eye_color:Mapped[str] = mapped_column(String)
    films:Mapped[str] = mapped_column(String)
    gender:Mapped[str] = mapped_column(String)
    hair_color:Mapped[str] = mapped_column(String)
    height:Mapped[str] = mapped_column(String)
    homeworld:Mapped[str] = mapped_column(String)
    mass:Mapped[str] = mapped_column(String)
    name:Mapped[str] = mapped_column(String)
    skin_color:Mapped[str] = mapped_column(String)
    species:Mapped[str] = mapped_column(String)
    starships:Mapped[str] = mapped_column(String)
    vehicles:Mapped[str] = mapped_column(String)

async def close_orm():
    await engine.dispose()

async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



if __name__ == '__main__':
    asyncio.run(init_orm())