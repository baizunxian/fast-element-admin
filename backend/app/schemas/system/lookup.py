import typing

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class LookupIn(BaseModel):
    """字典保存"""

    id: typing.Optional[int] = Field(None, description="字典id")
    code: str = Field(..., description="字典code")
    description: typing.Optional[str] = Field(None, description="字典描述")


class LookupQuery(BaseSchema):
    code: typing.Optional[str] = Field(None, description="字典code")


class LookupId(BaseSchema):
    id: int = Field(None, description="字典id")


class LookupValueQuery(BaseSchema):
    code: typing.Optional[str] = Field(None, description="字典code")
    lookup_id: typing.Optional[str] = Field(None, description="lookup_id")

    # @root_validator(pre=True)
    # def root_validator(cls, data):
    #     code = data.get('code', None)
    #     lookup_id = data.get('lookup_id', None)
    #     if not code:
    #         raise ParameterError('编码不能为空！')
    #     if not lookup_id:
    #         raise ParameterError('数据字典id不能为空！')
    #     return data


class LookupValueIn(BaseModel):
    """字典值保存"""
    id: int = Field(None, description="字典id")
    lookup_id: int = Field(None, description="字典id")
    lookup_code: typing.Optional[str] = Field(..., description="字典code")
    lookup_value: typing.Optional[str] = Field(..., description="字典value")
    ext: typing.Optional[str] = Field(None, description="备注")
    display_sequence: typing.Optional[int] = Field(None, description="显示顺序")
    description: typing.Optional[str] = Field(None, description="描述")
