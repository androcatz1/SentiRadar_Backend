import os
import psycopg2
from dotenv import load_dotenv
from app.config.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
load_dotenv()

def get_connection():
    if not Settings.DATABASE_URL_STATIC:
        raise ValueError("DATABASE_URL not found in environment")
    
    return psycopg2.connect(Settings.DATABASE_URL_STATIC)


def get_connection_time_series():
    if not Settings.DATABASE_URL:
        raise ValueError("DATABASE_URL not found in environment")
    
    return psycopg2.connect(Settings.DATABASE_URL)
    

engine = create_async_engine(Settings.DATABASE_URL_STATIC, pool_size=10, max_overflow=5)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# direct connection
async def get_db_static():
    async with async_session() as session:
        yield session    

engine_ts = create_async_engine(Settings.DATABASE_URL, pool_size=10, max_overflow=5)
async_session_ts = async_sessionmaker(engine_ts, expire_on_commit=False)

# direct connection
async def get_db_ts():
    async with async_session_ts() as session:
        yield session            