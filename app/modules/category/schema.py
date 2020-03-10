"""schema

Category Module Response Schema

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-04 10:04:19
"""

from flask_restplus_patched import ModelSchema
from flask_marshmallow import base_fields
from .model import *

class CategorySchema(ModelSchema):
    """
    Category schema
    """
    class Meta:
        model = Category

class CategoryListPagerSchema(CategorySchema):
    """
    Category pager schema
    """
    total = base_fields.Integer() 
    rows = base_fields.Nested(CategorySchema, many=True)
    class Meta:
        pass

class CategoryFieldSchema(ModelSchema):
    """
    Category Field schema
    """
    title = base_fields.String() 
    field = base_fields.String() 
    class Meta:
        pass