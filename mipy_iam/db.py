import os, logging, asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

import mipy_env
import mipy_log

######### module public
Base = declarative_base()
    
def init() -> str:
    sqlite_path = mipy_env.get_or_ask_and_wait_for_param("SQLITE_PATH", default="var/db.sqlite3", value_type=str)
    return sqlite_path 
        
async def close():
    global _db_initialized, _engine, _async_sessionmaker
    
    if _engine != None:
        await _engine.dispose()     
        
        _db_initialized = False
        _async_sessionmaker = None
        _engine = None
        
async def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    await _init()
    return _async_sessionmaker

######### module private
# Function to get an async database session
async def _init():
    global _db_initialized, _async_sessionmaker, _engine
    
    if _db_initialized:
        return
    
    # Replace with your async database URL
    log = mipy_log.create(__name__)
    log.info("Setting up database...")
    sqlite_path = os.environ.get("SQLITE_PATH", None) 
    if sqlite_path is None:
        raise ValueError(f'Missing env var "SQLITE_PATH"') #mipy_env.get_or_ask_and_wait_for_param("SQLITE_PATH", default="var/db.sqlite3", value_type=str)
    
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"

    _engine = create_async_engine(DATABASE_URL, echo=False)
    _async_sessionmaker =  async_sessionmaker(_engine, expire_on_commit=False)

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _db_initialized = True

######### module private
_db_initialized = False
_async_sessionmaker:async_sessionmaker[AsyncSession]|None = None
_engine:AsyncEngine|None = None