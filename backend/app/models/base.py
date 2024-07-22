import time
import typing
from math import ceil

from loguru import logger
from sqlalchemy import Boolean, DateTime, func, select, update, delete, insert, Select, \
    Executable, Result, String, ClauseList, BigInteger, literal_column, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import mapped_column, noload

from app.utils.serialize import default_serialize
from app.db.sqlalchemy import async_transaction
from app.utils.context import AppTraceId, SQLAlchemySession, FastApiRequest

T = typing.TypeVar("T", Select, "Query[Any]")


@as_declarative()
class Base:
    """ 基本表 """
    # db.scalar(sql) 返回的是标量(原始数据) <models.department.Department object at 0x000002F2C2D22110>
    # db.execute(sql) 返回的是元组 (<models.department.Department object at 0x000002F2C2D22110>)
    # db.scalars(sql).all()  [<models...>, <models...>, <models...>]
    # db.execute(sql).fetchall()  [(<models...>,), (<models...>,), (<models...>,)]
    __abstract__ = True

    __name__: str  # 表名
    __table_args__ = {"mysql_charset": "utf8"}  # 设置表的字符集

    __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    # @declared_attr
    # def __tablename__(cls) -> str:
    #     """将类名小写并转化为表名 __tablename__"""
    #     return cls.__name__.lower()

    id = mapped_column(BigInteger(), nullable=False, primary_key=True, autoincrement=True, comment='主键')
    creation_date = mapped_column(DateTime(), default=func.now(), comment='创建时间')
    created_by = mapped_column(BigInteger, comment='创建人ID')
    updation_date = mapped_column(DateTime(), default=func.now(), onupdate=func.now(), comment='更新时间')
    updated_by = mapped_column(BigInteger, comment='更新人ID')
    enabled_flag = mapped_column(Boolean(), default=1, nullable=False, comment='是否删除, 0 删除 1 非删除')
    trace_id = mapped_column(String(255), comment="trace_id")

    @classmethod
    async def get(cls, id: typing.Union[int, str], to_dict: object = False) -> typing.Union["Base", typing.Dict, None]:
        """
        :param id: 查询id
        :param to_dict: 转字典
        :return: 模型对象 <models...>
        """
        if not id:
            return None
        q = []
        if hasattr(cls, "enabled_flag"):
            q.append(cls.enabled_flag == 1)
        sql = select(cls).where(cls.id == id, *q)
        result = (await cls.execute(sql)).scalar()
        return result if not to_dict else cls.unwrap_scalars(result)

    @classmethod
    async def get_all(cls) -> typing.Optional[typing.Any]:
        """
        :return: 返回所有数据  list[dict]
        """
        q = []
        if hasattr(cls, "enabled_flag"):
            q.append(cls.enabled_flag == 1)
        stmt = select(cls.get_table_columns()).where(*q)
        return await cls.get_result(stmt)

    @classmethod
    async def create_or_update(cls, params: typing.Union[typing.Dict], to_dict: bool = True) -> typing.Dict[
        typing.Text, typing.Any]:
        """
        :param params: 更新数据 dict
        :return: 更新后的数据 dict
        """
        if not isinstance(params, dict):
            raise ValueError("更新参数错误！")
        params = await cls.handle_params(params)
        id = params.get("id", None)
        exist_data = await cls.get(id)
        if exist_data:
            result = await cls.update(params, to_dict=to_dict)
        else:
            result = await cls.create(params, to_dict=to_dict)

        return result

    @classmethod
    async def create(cls, params: typing.Dict, to_dict: bool = False) -> typing.Union["Base", typing.Dict]:
        """
        插入数据
        :param params: 批量插入数据
        :param to_dict: 是否转字典
        :return: 插入数量
        """
        if not isinstance(params, dict):
            raise ValueError("参数错误")
        params = await cls.handle_params(params)
        stmt = insert(cls).values(**params)
        result = await cls.execute(stmt)
        (primary_key,) = result.inserted_primary_key
        params["id"] = primary_key
        return await cls.get(primary_key, to_dict=to_dict)

    @classmethod
    async def update(cls, params: typing.Dict, to_dict: bool = False) -> typing.Union['Base', typing.Dict]:
        if not isinstance(params, dict):
            raise ValueError("参数错误")
        params = await cls.handle_params(params)
        update_id = params.get("id", None)
        if not update_id:
            raise ValueError("id不能为空")

        stmt = update(cls).where(cls.id == update_id).values(**params)
        await cls.execute(stmt)
        return await cls.get(update_id, to_dict=to_dict)

    @classmethod
    async def batch_create(cls, params: typing.List) -> int:
        """
        批量插入数据
        :param params: 批量插入数据
        :return: 插入数量
        """
        if not params:
            return 0
        if not isinstance(params, list):
            raise ValueError("参数错误，参数必须为列表")
        params = await cls.handle_params(params)
        stmt = insert(cls).values(params)
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    async def handle_params(cls, params: typing.Any) -> typing.Any:
        """
        :param params: 参数列表
        :return: 过滤好的参数
        """
        if isinstance(params, dict):
            params = {key: value for key, value in params.items() if hasattr(cls, key)}
            if hasattr(cls, "trace_id") and AppTraceId.get():
                params["trace_id"] = AppTraceId.get()
        elif isinstance(params, list):
            params = [await cls.handle_params(p) for p in params]
        return params

    @classmethod
    async def delete(cls, id: typing.Union[int, str], _hard: bool = False) -> int:
        """
        :param id: 删除数据id
        :param _hard:  False 逻辑删除， Ture 物理删除
        :return: sql影响行数
        """
        if not id:
            return 0

        if _hard is False and hasattr(cls, "enabled_flag"):
            stmt = update(cls).where(cls.id == id, cls.enabled_flag == 1).values(enabled_flag=0)
        else:
            stmt = delete(cls).where(cls.id == id)
        result = await cls.execute(stmt)
        return result.rowcount

    @classmethod
    @async_transaction
    async def execute(cls, stmt: Executable, params: typing.Any = None) -> Result[
        typing.Any]:
        """
        执行sql
        :param stmt: sqlalchemy Executable 对象
        :param params: params 参数
        :return:
        """
        session = SQLAlchemySession.get()
        return await session.execute(stmt, params)

    @classmethod
    async def pagination(cls, stmt: Select) -> typing.Dict[str, typing.Any]:
        """
        分页查询
        :param stmt: select对象
        :return:
        """
        return await cls.parse_pagination(stmt)

    @classmethod
    def get_table_columns(cls, exclude: set = None) -> ClauseList:
        """
        获取模型所有字段
        exclude: 排除字段  {"name"}
        :return:
        """
        exclude = exclude if exclude else set()
        return ClauseList(*[i for i in cls.__table__.columns if i.name not in exclude])

    @classmethod
    async def get_result(cls, stmt: Select, first=False) -> typing.Any:
        """
        <models...> or  <Row...>
        获取查询结果转转为dict

        first=True：
        {
            "key": "value"
            ...
        }
        first=False：
        [
            {
                "key1": "value1"
                ...
            },
            {
                "key2": "value2"
                ...
            }
        ]

        :param stmt: sqlalchemy Executable 对象
        :param first: 是否只取一条
        :return:
        """
        result = await cls.execute(stmt)
        start_time = time.time()
        data = result.first() if first else result.all()
        logger.debug(f"get_result 耗时:{time.time() - start_time}")
        # 直接使用pydantic的模型验证
        # fields = {key: (type(default_serialize(value)), default_serialize(value)) for key, value in data.items()}
        # return pydantic.create_model("__Row__", **fields).model_validate(data)
        return cls.unwrap_scalars(data) if data else None

    @staticmethod
    @async_transaction
    async def parse_pagination(
            query: select,
            page: int = None,
            page_size: int = None) -> typing.Dict[str, typing.Any]:
        """
        统一分页处理
        :param query: query
        :param page: query
        :param page_size: query
        :return:
        """
        session: AsyncSession = SQLAlchemySession.get()
        request = FastApiRequest.get()
        if request.method == 'POST':
            request_json = request.scope.get('request_body', {})
            page = int(request_json.get('page', 1)) if not page else page
            page_size = min(int(request_json.get('pageSize', 10)), 1000) if not page_size else page_size
        else:
            page = request.query_params.get('page', 1) if not page else page
            page_size = min(request.query_params.get('pageSize', default=10),
                            1000) if not page_size else page_size

        (total,) = (await session.execute(Base.count_query(query))).scalars()
        start_time = time.time()
        result = (await session.execute(Base.paginate_query(query, page=page, page_size=page_size))).fetchall()
        logger.debug(f"parse_pagination 耗时:{time.time() - start_time}")
        result = Base.unwrap_scalars(result)
        total_page = int(ceil(float(total) / page_size))
        pagination = {
            'rowTotal': total,
            'pageSize': page_size,
            'page': page,
            'pageTotal': total_page,
            'rows': result,
        }

        return pagination

    @staticmethod
    def count_query(query: Select) -> Select:
        """
        获取count sql
        :param query: sql
        :return:
        """
        count_subquery = typing.cast(typing.Any, query.order_by(None)).options(noload("*")).subquery()
        return select(func.count(literal_column("*"))).select_from(count_subquery)

    @staticmethod
    def paginate_query(query: T, page: int, page_size: int) -> T:
        """
        获取分页sql
        :param query:
        :param page: 页数
        :param page_size: 每页大小
        :return:
        """
        return query.limit(page_size).offset(page_size * (page - 1))

    @staticmethod
    def len_or_none(obj: typing.Any) -> typing.Optional[int]:
        """有数据返回长度 没数据返回None"""
        try:
            return len(obj)
        except TypeError:
            return None

    @staticmethod
    def unwrap_scalars(items: typing.Union[typing.Sequence[Row], Row]) -> typing.Union[
        typing.List[typing.Dict[typing.Text, typing.Any]], typing.Dict[str, typing.Any]]:
        """
        数据库Row对象数据序列化为字典
        :param items: 数据返回数据 [Row(...)]
        :return:
        """
        # if isinstance(items, typing.Iterable) and not isinstance(items, Row):
        #     return [default_serialize(item) for item in items]
        return default_serialize(items)
