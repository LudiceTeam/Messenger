from main_models import main_table,metadata_obj
from sqlalchemy import select,exc
from typing import Optional,List 
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
#from chats_models import metadata_obj,chats_table
import asyncio
from datetime import datetime,timedelta




load_dotenv()


async_engine = create_async_engine(
   f"postgresql+asyncpg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/messenger_main", 
    pool_size=20,          
    max_overflow=50,        
    pool_recycle=3600,    
    pool_pre_ping=True,     
    echo=False
)

AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)


async def get_all_data():
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table)
            res = await conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise Exception(f"Error : {e}")  

async def is_user_exists(username:str) -> bool:
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table.c.username).where(main_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            return data is not None
        except Exception as e:
            raise Exception(f"Error : {e}")        

async def create_user_data(username:str,psw:str) -> bool:
    if await is_user_exists(username):
        return False 
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = main_table.insert().values(
                    username = username,
                    password = psw,
                    avatar = "",
                    state = ""
                )
                await conn.execute(stmt)
            except exc.SQLAlchemyError:
                raise Exception("Error while executing")

async def login(username:str,try_psw:str) -> bool:
    if not await is_user_exists(username):
        return False
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table.c.password).where(main_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            return str(data) == try_psw
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")            
            

async def change_user_avatar(username:str,new_avatar:str):
    if not await is_user_exists(username):
        return
    async with AsyncSession(async_engine) as conn:
        async with conn.begin():
            try:
                stmt = main_table.update().where(main_table.c.username == username).values(
                    avatar = new_avatar
                )
                await conn.execute(stmt)
            except  exc.SQLAlchemyError:
                raise exc.SQLAlchemyError("Error while exeuting")   

async def get_user_avatar(username:str) -> str:
    if not await is_user_exists(username):
        return
    async with AsyncSession(async_engine) as conn:
        try:
            stmt = select(main_table.c.avatar).where(main_table.c.username == username)
            res = await conn.execute(stmt)
            data = res.scalar_one_or_none()
            return str(data)
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")   

async def get_user_state(username:str) -> str:
    pass
                 
        
        
            