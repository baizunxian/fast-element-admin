# -*- coding: utf-8 -*-
# @author: 小白
from typing import Callable

import fastapi
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

from app.utils.context import FastApiRequest


class ContextIncludedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # 请求日志的初始化操作
            try:
                body_form = await request.form()
            except:
                body_form = None

            body = None
            try:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        body = await request.json()
                    except:
                        pass
                        if body_bytes:
                            try:
                                body = body_bytes.decode('utf-8')
                            except:
                                body = body_bytes.decode('gb2312')
            except:
                pass

            request.scope.setdefault("request_form", body_form)
            request.scope.setdefault("request_body", body)
            FastApiRequest.set(request)

            # 这里记录下请求入口的时候相关的日志信息

            response: Response = await original_route_handler(request)

            return response

        return custom_route_handler


class APIRouter(fastapi.APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route_class = ContextIncludedRoute
