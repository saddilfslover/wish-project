from sqlalchemy import ForeignKey, String, BigInteger, Text, Float
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class WishItem(Base):
    __tablename__ = 'wish_items'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    priority: Mapped[int] = mapped_column(default=3)  # 1-высокий, 2-средний, 3-низкий
    link: Mapped[str] = mapped_column(String(512), nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all) 