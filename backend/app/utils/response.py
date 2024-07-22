# -*- coding: utf-8 -*-
# @author: xiaobai

import typing
from enum import Enum, unique

import orjson
from starlette import status
from starlette.responses import JSONResponse

from app.utils.context import AppTraceId
from app.utils.serialize import default_serialize


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_PASSTHROUGH_DATETIME,
            default=default_serialize
        )


@unique
class BaseCodeEnum(Enum):

    @property
    def code(self):
        """获取状态吗"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]

    @staticmethod
    def get_success_code():
        return 0

    @staticmethod
    def get_success_msg():
        return "OK"

    @staticmethod
    def get_fail_code():
        return -1

    @staticmethod
    def get_fail_msg():
        return "操作失败"


class HttpResponse:

    @staticmethod
    async def success(data: typing.Any = None,
                      code: int = BaseCodeEnum.get_success_code(),
                      msg: str = BaseCodeEnum.get_success_msg(),
                      http_code: int = status.HTTP_200_OK,
                      headers: typing.Optional[dict] = None) -> ORJSONResponse:
        """
        通用结果返回
        :param data: 返回数据
        :param code: 状态码
        :param http_code: http状态码
        :param msg: 返回消息
        :param headers: 响应头
        :return:
        """

        if data is None:
            data = {}

        success = True if code == BaseCodeEnum.get_success_code() else False
        content = dict(code=code, msg=msg, data=data, success=success, trace_id=AppTraceId.get())
        content = default_serialize(content)
        return ORJSONResponse(status_code=http_code, content=content, headers=headers)

    @staticmethod
    async def fail(data: typing.Any = None,
                   code: int = BaseCodeEnum.get_fail_code(),
                   msg: str = BaseCodeEnum.get_fail_msg(),
                   http_code: int = status.HTTP_200_OK,
                   headers: typing.Optional[dict] = None) -> ORJSONResponse:
        """
        通用结果返回
        :param data: 返回数据
        :param code: 状态码
        :param http_code: http状态码
        :param msg: 返回消息
        :param headers: 响应头
        :return:
        """

        if data is None:
            data = {}

        success = True if code == BaseCodeEnum.get_fail_code() else False
        content = dict(code=code, msg=msg, data=data, success=success, trace_id=AppTraceId.get())
        content = default_serialize(content)
        return ORJSONResponse(status_code=http_code, content=content, headers=headers)

    @staticmethod
    async def resp_200(*, data: typing.Any = '', msg: str = "Success") -> dict:
        return {'code': 200, 'data': data, 'msg': msg}

    @staticmethod
    async def resp_400(code: int = 400, data: str = None, msg: str = "请求错误(400)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'code': code, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_401(*, data: str = None, msg: str = "未授权，请重新登录(401)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code': 401, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_403(*, data: str = None, msg: str = "拒绝访问(403)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'code': 403, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_404(*, data: str = None, msg: str = "请求出错(404)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'code': 404, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_422(*, data: str = None, msg: typing.Union[list, dict, str] = "不可处理的实体") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                              content={'code': 422, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_500(*, data: str = None, msg: typing.Union[list, dict, str] = "服务器错误(500)") -> ORJSONResponse:
        return ORJSONResponse(headers={'Access-Control-Allow-Origin': '*'},
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              content={'code': 500, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_502(*, data: str = None, msg: str = "网络错误(502)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={'code': 502, 'msg': msg, 'data': data})

    # ------------------------------------------- 以下不常用 -------------------------------------------
    @staticmethod
    async def resp_406(*, data: str = None, msg: str = "请求的格式不可得(406)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                              content={'code': 406, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_408(*, data: str = None, msg: str = "请求超时(408)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_408_REQUEST_TIMEOUT,
                              content={'code': 408, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_410(*, data: str = None, msg: str = "请求的资源被永久删除，且不会再得到的(410)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_410_GONE, content={'code': 410, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_501(*, data: str = None, msg: str = "服务未实现(501)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                              content={'code': 501, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_503(*, data: str = None, msg: str = "服务不可用(503)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                              content={'code': 503, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_504(*, data: str = None, msg: str = "网络超时(504)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                              content={'code': 504, 'msg': msg, 'data': data})

    @staticmethod
    async def resp_505(*, data: str = None, msg: str = "HTTP版本不受支持(505)") -> ORJSONResponse:
        return ORJSONResponse(status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
                              content={'code': 505, 'msg': msg, 'data': data})
