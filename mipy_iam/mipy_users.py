from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from mipy_iam.mipy_db import Base, get_sessionmaker
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mipy_log

# Define the User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class UserData(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True 
        
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    
router = APIRouter()

# CRUD functions for User
# Create a User
@router.post("/users/", response_model=UserData)
async def create(user: UserCreate) -> UserData:
    create_session = await get_sessionmaker()
    async with create_session() as session:
        async with session.begin():
            hashed_password = user.password # TODO
            new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
            session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserData.from_orm( new_user )


# Get a User by ID
@router.get("/users/{user_id}", response_model=UserData)
async def by_id(user_id: int) -> UserData:
    create_session = await get_sessionmaker()
    
    async with create_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return UserData.from_orm( result.scalars().first() )

# Get all Users
@router.get("/users/", response_model=list[UserData])
async def all() -> list[UserData]:
    create_session = await get_sessionmaker()    
    async with create_session() as session:
        result = await session.execute(select(User))
        return [ UserData.from_orm( user ) for user in result.scalars().all() ]

# Update a User
@router.put("/users/{user_id}", response_model=UserData)
async def update(user_id: int, user_update: UserUpdate) -> UserData:
    create_session = await get_sessionmaker()
    
    async with create_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            
            # update the values
            for key, value in user_update.dict(exclude_unset=True).items():
                if key == "password":
                    value = value # TODO
                setattr(user, key, value)
            await session.commit()
    
        async with session.begin():
            await session.refresh(user)
            return UserData.from_orm( user )


# Delete a User
@router.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: int) -> None:
    create_session = await get_sessionmaker()
    
    async with create_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            await session.delete(user)
            await session.commit()
