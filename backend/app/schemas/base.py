# -*- coding: utf-8 -*-
# @author: xiaobai
from pydantic import BaseModel, field_validator


class BaseSchema(BaseModel):
    def model_dump(self, *args, **kwargs):
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return super(BaseSchema, self).model_dump(*args, **kwargs)

    @field_validator('*', mode="before")
    def blank_strings(cls, v):
        if v == "":
            return None
        return v
