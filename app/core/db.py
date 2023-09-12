from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core import settings

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [str(column.name) for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class SessionManager:
    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def refresh(self) -> None:
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False,
            future=True,
        )


async def get_async_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


metadata = MetaData(naming_convention=convention)
Base = declarative_base(cls=PreBase, metadata=metadata)
