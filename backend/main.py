# -*- coding: utf-8 -*-
# @author: xiaobai
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.corelibs.logger import init_logger, logger
from app.db import redis_pool
from app.init.cors import init_cors
from app.init.exception import init_exception
from app.init.middleware import init_middleware
from app.init.routers import init_router
from config import config


@asynccontextmanager
async def start_app(app: FastAPI):
    """ 注册中心 """
    # register_mount(app)  # 挂载静态文件
    redis_pool.init_by_config(config=config)
    init_logger()
    logger.info("日志初始化成功！！!")  # 初始化日志

    yield

    await redis_pool.redis.close()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="vue-fastapi-admin",
                           config=config,
                           description=config.SERVER_DESC,
                           version=config.SERVER_VERSION,
                           lifespan=start_app)
    init_exception(app)  # 注册捕获全局异常
    init_router(app)  # 注册路由
    init_middleware(app)  # 注册请求响应拦截
    init_cors(app)  # 初始化跨域

    return app


app = create_app()

# gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8101
if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=9100, reload=True)
