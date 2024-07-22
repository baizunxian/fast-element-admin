# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class MenuIn(BaseModel):
    id: int = Field(None, description='id')
    path: typing.Optional[str] = Field(..., description='路径')
    name: typing.Optional[str] = Field(..., description='组件名称')
    component: typing.Optional[str] = Field(..., description='组件路径')
    title: typing.Optional[str] = Field(..., description='路由名称')
    isLink: typing.Optional[bool] = Field(False,
                                          description='是否是链接 开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`')
    isHide: typing.Optional[bool] = Field(False, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isKeepAlive: typing.Optional[bool] = Field(True, description='菜单是否隐藏（菜单不显示在界面，但可以进行跳转）')
    isAffix: typing.Optional[bool] = Field(False, description='是否固定')
    isIframe: typing.Optional[bool] = Field(False, description='是否内嵌')
    icon: typing.Optional[str] = Field("", description='菜单图标')
    parent_id: typing.Optional[str] = Field(..., description='父级菜单id')
    redirect: typing.Optional[str] = Field(None, description='重定向路由')
    sort: typing.Optional[int] = Field(0, description='排序')
    menu_type: typing.Optional[int] = Field(..., description='菜单类型')
    active_menu: typing.Optional[str] = Field(None, description='显示页签')


class MenuUpdate(MenuIn):
    pass


class MenuDel(BaseModel):
    id: int = Field(..., title="id", description='id')


class MenuViews(BaseModel):
    menu_id: int = Field(..., title="id", description='菜单id')


class Menu(BaseSchema):
    name: typing.Optional[str] = Field(None, description='组件名称')
