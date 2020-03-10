"""schema

Response Schema

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from flask_restplus_patched import ModelSchema
from flask_marshmallow import base_fields
from .model import *

class ConfigsSchema(ModelSchema):
    """
    Configs schema
    """
    class Meta:
        model = Configs

class ConfigsListPagerSchema(ModelSchema):
    """
    Configs list pager schema
    """
    total = base_fields.Integer() 
    rows = base_fields.Nested(ConfigsSchema, many=True)
    class Meta:
        pass

class ConfigsModelsSchema(ModelSchema):
    """
    Get Models list
    """
    model = base_fields.String() 
    module = base_fields.String() 
    module_name = base_fields.String() 
    tablename = base_fields.String() 
    model = base_fields.String() 
    columns = base_fields.List(base_fields.String(), many=True)
    class Meta:
        pass

