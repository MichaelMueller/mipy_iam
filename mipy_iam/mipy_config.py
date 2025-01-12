from sqlalchemy import Column, String, inspect
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from mipy_iam.mipy_db import Base, get_sessionmaker
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Define the Config model
class Config(Base):
    __tablename__ = "config"

    key = Column(String, primary_key=True, index=True, nullable=False)
    value = Column(String, nullable=False)

class ConfigItem(BaseModel):
    key: str
    value: str
    class Config:
        orm_mode = True 
        
router = APIRouter()

# Set a configuration key-value pair
@router.api_route("/config_items/", methods=["POST", "PUT"], response_model=None)
async def set(config_item: ConfigItem) -> None:    
    create_session = await get_sessionmaker()

    async with create_session() as session:
        async with session.begin():
            existing_entry = await session.execute(select(Config).where(Config.key == config_item.key))
            config = existing_entry.scalars().first()
            if config:
                config.value = config_item.value
            else:
                config = Config(key=config_item.key, value=config_item.value)
                session.add(config)
        await session.commit()

# Get the value of a configuration key
@router.get("/config_items/{key}", response_model=ConfigItem)
async def get_config(key: str) -> ConfigItem:
    create_session = await get_sessionmaker()

    async with create_session() as session:
        result = await session.execute(select(Config).where(Config.key == key))
        config = result.scalars().first()
        return ConfigItem.from_orm( config )

# Remove a configuration key
@router.delete("/config_items/{key}", response_model=None)
async def remove_config(key: str) -> None:
    create_session = await get_sessionmaker()

    async with create_session() as session:
        async with session.begin():
            result = await session.execute(select(Config).where(Config.key == key))
            config = result.scalars().first()
            await session.delete(config)
        await session.commit()

@router.get("/config_items/", response_model=list[ConfigItem])
async def all() -> list[ConfigItem]:
    create_session = await get_sessionmaker()    
    async with create_session() as session:
        result = await session.execute(select(Config))
        return [ ConfigItem.from_orm( config_item ) for config_item in result.scalars().all() ]