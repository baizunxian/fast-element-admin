# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema
from app.utils.des import decrypt_rsa_password


class UserIn(BaseModel):
    id: typing.Optional[int] = Field(None, title="id", description='id')
    username: typing.Optional[str] = Field(..., title="用户名不能为空！", description='用户名')
    nickname: typing.Optional[str] = Field(..., title="用户昵称不能为空！", description='用户昵称')
    email: typing.Optional[str] = Field(None, description='邮箱')
    user_type: typing.Optional[int] = Field(None, description='用户类型')
    status: typing.Optional[int] = Field(None, description='是否禁用')
    remarks: typing.Optional[str] = Field(None, description='用户描述')
    avatar: typing.Optional[str] = Field(None, description='头像')
    tags: typing.List = Field(None, description='标签')
    roles: typing.List = Field(None, description='权限')
    password: typing.Optional[str] = Field(description='标签', default=decrypt_rsa_password("123456"))


class UserUpdate(BaseModel):
    pass


class UserDel(BaseModel):
    id: int = Field(..., title="id", description='id')


class UserQuery(BaseSchema):
    username: typing.Optional[str] = Field(None, description='用户名')
    nickname: typing.Optional[str] = Field(None, description='昵称')
    user_ids: typing.List[int] = Field(None, description='用户id')


class UserLogin(BaseModel):
    username: typing.Optional[str] = Field(..., description='用户名')
    password: typing.Optional[str] = Field(..., description='密码')


class UserResetPwd(BaseModel):
    id: int = Field(..., description='用户id')
    old_pwd: typing.Optional[str] = Field(..., description='旧密码')
    new_pwd: typing.Optional[str] = Field(..., description='新密码')
    re_new_pwd: typing.Optional[str] = Field(..., description='二次输入新密码')


class UserLoginRecordIn(BaseModel):
    token: typing.Optional[str] = Field(None, description='token')
    code: typing.Optional[str] = Field(None, description="账号")
    user_id: typing.Optional[int] = Field(None, description="用户id")
    user_name: typing.Optional[str] = Field(None, description="用户名称")
    logout_type: typing.Optional[str] = Field(None, description="登出类型")
    login_type: typing.Optional[str] = Field(None, description="登录类型")
    login_time: typing.Optional[str] = Field(None, description="登录时间")
    logout_time: typing.Optional[str] = Field(None, description="登出时间")
    login_ip: typing.Optional[str] = Field(None, description="登录ip")
    ret_msg: typing.Optional[str] = Field(None, description="返回信息")
    ret_code: typing.Optional[str] = Field(None, description="返回code")
    address: typing.Optional[str] = Field(None, description="地址")
    source_type: typing.Optional[str] = Field(None, description="来源")


class UserLoginRecordQuery(BaseModel):
    token: typing.Optional[str] = Field(None, description='token')
    code: typing.Optional[str] = Field(None, description="账号")
    user_id: typing.Optional[int] = Field(None, description="用户id")
    user_name: typing.Optional[str] = Field(None, description="用户名称")
    logout_type: typing.Optional[str] = Field(None, description="登出类型")
    login_type: typing.Optional[str] = Field(None, description="登录类型")
    login_time: typing.Optional[str] = Field(None, description="登录时间")
    logout_time: typing.Optional[str] = Field(None, description="登出时间")
    login_ip: typing.Optional[str] = Field(None, description="登录ip")
    ret_msg: typing.Optional[str] = Field(None, description="返回信息")
    ret_code: typing.Optional[str] = Field(None, description="返回code")
    address: typing.Optional[str] = Field(None, description="地址")
    source_type: typing.Optional[str] = Field(None, description="来源")
