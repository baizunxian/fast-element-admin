# -*- coding: utf-8 -*-
# @author: xiaobai
import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime, Boolean, insert, update, select
from sqlalchemy.orm import aliased

from app.models.api_models import ModuleInfo, ProjectInfo
from app.models.base import Base
from app.models.system_models import User
from app.schemas.api.timed_task import TimedTasksQuerySchema


class TimedTask(Base):
    """定时任务表"""
    __tablename__ = 'celery_periodic_task'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=True, comment='定时任务名')
    task = Column(String(200), comment='任务路径')
    args = Column(String(200), comment='参数')
    kwargs = Column(String(200), comment='关键字参数')
    queue = Column(String(200), comment='队列')
    exchange = Column(String(200), comment='交换')
    routing_key = Column(String(200), comment='路由密钥')
    expires = Column(DateTime, comment='到期时间')
    one_off = Column(Boolean, comment='执行一次')
    start_time = Column(DateTime, comment='开始时间')
    enabled = Column(String(200), comment='是否启用, 1启动，0停用', default=0)
    last_run_at = Column(String(200), comment='上次运行时间')
    total_run_count = Column(String(200), comment='运行总次数', default=0)
    date_changed = Column(DateTime, comment='更改日期')
    description = Column(String(200), comment='备注')
    crontab_id = Column(Integer, comment='定时器id')
    crontab = Column(Integer, comment='crontab 表达式')
    interval_id = Column(Integer, comment='间隔id')
    interval_every = Column(Integer, comment='间隔时间')
    interval_period = Column(String(24), comment='间隔类型')
    task_type = Column(String(255), nullable=False, comment="crontab interval")
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=False, comment='模块id')
    suite_id = Column(Integer, nullable=False, comment='套件id')
    case_env_id = Column(Integer, nullable=False, comment='case_env_id 用例环境')
    case_ids = Column(String(255), nullable=False, comment='用例集合')
    ui_env_id = Column(Integer, nullable=False, comment='case_env_id 用例环境')
    ui_ids = Column(String(255), nullable=False, comment='ui用例集合')
    script_ids = Column(String(255), nullable=False, comment='脚本id')
    task_tags = Column(String(255), nullable=False, comment='任务标签')
    remarks = Column(String(255), nullable=False, comment='任务描述')

    @classmethod
    async def get_list(cls, params: TimedTasksQuerySchema):
        q = [cls.enabled_flag == 1]
        u = aliased(User)
        if params.id:
            q.append(cls.id == params.id)
        if params.name:
            q.append(cls.name.like('%{}%'.format(params.name)))
        if params.created_by_name:
            q.append(u.nickname.like('%{}%'.format(params.created_by_name)))
        if params.user_ids:
            q.append(cls.created_by.in_(params.user_ids))
        if params.created_by:
            q.append(cls.created_by == params.created_by)
        if params.project_ids:
            q.append(cls.project_id.in_(params.project_ids))

        stmt = select(cls).where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(User, User.id == cls.updated_by) \
            .with_only_columns(*cls.get_table_columns(),
                               u.nickname.label('created_by_name'),
                               User.nickname.label('updated_by_name'),
                               ProjectInfo.name.label('project_name'),
                               ModuleInfo.name.label('module_name')) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_task_by_name(cls, name):
        """获取任务名存在的个数"""
        stmt = select(cls).where(cls.name == name, cls.enabled_flag == 1)
        return await cls.get_result(stmt)


class Crontab(Base):
    """crontab 表"""
    __tablename__ = 'celery_crontab_schedule'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    minute = Column(String(200), comment='分钟')
    hour = Column(String(200), comment='小时')
    day_of_week = Column(String(200), comment='日期')
    day_of_month = Column(String(200), comment='月份')
    month_of_year = Column(String(200), comment='年')
    timezone = Column(String(200), comment='时区', default='Asia/Shanghai')

    @classmethod
    async def get_crontab_by_parameter(cls, minute, hour, day_of_week, day_of_month, month_of_year):
        stmt = select(cls).where(cls.minute == minute, cls.hour == hour, cls.day_of_week == day_of_week,
                                 cls.day_of_month == day_of_month, cls.month_of_year == month_of_year)
        return await cls.get_result(stmt, first=True)


class IntervalSchedule(Base):
    """时间间隔 表"""
    __tablename__ = 'celery_interval_schedule'

    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    MICROSECONDS = 'microseconds'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    every = Column(Integer, comment='区间数')
    period = Column(String(24), comment='间隔单位')

    @classmethod
    async def get_interval_by_parameter(cls, every, period):
        stmt = select(cls).where(cls.every == every, cls.period == period)
        return await cls.get_result(stmt, first=True)


class PeriodicTaskChanged(Base):
    """定时任务更新表"""
    __tablename__ = 'celery_periodic_task_changed'

    id = Column(Integer(), nullable=False, primary_key=True, autoincrement=True)
    last_update = Column(DateTime, comment='到期时间')

    @classmethod
    async def update_changed(cls):
        stmt = select(cls).where(cls.id == 1).limit(1)
        s = cls.get_result(stmt, first=True)
        if s:
            stmt = update(cls).where(cls.id == 1).values(last_update=dt.datetime.now())
        else:
            stmt = insert(cls).values(id=1, last_update=dt.datetime.now())
        await cls.execute(stmt)
