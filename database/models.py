from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Асинхронное подключение (основное)
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Синхронное подключение для тестов
TEST_DATABASE_URL = "sqlite:///"

sync_engine = create_engine(
    TEST_DATABASE_URL, 
    echo=True
)

sync_session = sessionmaker(
    sync_engine, 
    expire_on_commit=False, 
    class_=Session
)

Base = declarative_base()