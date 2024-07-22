# -*- coding: utf-8 -*-
# @author: 小白
from contextvars import ContextVar
from typing import Optional

from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

AccessToken: ContextVar[Optional[str]] = ContextVar('AccessToken', default=None)
AppTraceId: ContextVar[Optional[str]] = ContextVar('AppTraceId', default=None)
SQLAlchemySession: ContextVar[Optional[AsyncSession]] = ContextVar('SQLAlchemySession', default=None)

FastApiRequest: ContextVar[Optional[Request]] = ContextVar('fastApiRequest', default=None)
