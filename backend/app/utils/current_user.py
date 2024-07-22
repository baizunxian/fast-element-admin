# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from app.corelibs.consts import TEST_USER_INFO
from app.db import redis_pool
from app.exceptions.exceptions import AccessTokenFail
from app.utils.context import AccessToken


async def current_user(token: str = None) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
    """根据token获取用户信息"""
    user_info = await redis_pool.redis.get(TEST_USER_INFO.format(AccessToken.get() if not token else token))
    if not user_info:
        raise AccessTokenFail()
    return user_info
