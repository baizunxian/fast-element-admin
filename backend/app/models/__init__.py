# -*- coding: utf-8 -*-
# @author: xiaobai
import asyncio

from loguru import logger
from app.db.sqlalchemy import engine
from app.models.base import Base


async def init_db():
    """
    初始化数据库
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
