"""schema

Response Schema
响应模式

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from .status import Status
from flask_restplus_patched import ModelSchema
from flask_marshmallow import base_fields

class BasicSchema(ModelSchema):
    status = base_fields.Integer(default=Status.SUCCESS.status) 
    message = base_fields.String(default=Status.SUCCESS.message) 
    data = base_fields.Raw()
    class Meta:
        pass

class BasicPagerSchema(ModelSchema):
    has_prev = base_fields.Boolean() 
    has_next = base_fields.Boolean() 
    pages = base_fields.Integer() 
    page = base_fields.Integer() 
    lst_size = base_fields.Integer()
    total = base_fields.Integer() 
    items = base_fields.Raw()
    class Meta:
        pass

class DeleteSchema(ModelSchema):
    delete = base_fields.Integer()
    class Meta:
        pass

class ResSchema(ModelSchema):
    res = base_fields.Integer()
    class Meta:
        pass