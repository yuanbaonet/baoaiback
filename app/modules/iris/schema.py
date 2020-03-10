"""schema

IRIS Module Response Schema

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
"""

from flask_restplus_patched import ModelSchema
from flask_marshmallow import base_fields
from .model import *

class IrisSchema(ModelSchema):
    """
    IRIS schema
    """
    class Meta:
        model = Iris

class IrisListPagerSchema(IrisSchema):
    """
    IRIS pager schema
    """
    total = base_fields.Integer() 
    rows = base_fields.Nested(IrisSchema, many=True)
    class Meta:
        pass

class IrisPredictSchema(ModelSchema):
    """
    IRIS pager schema
    """
    linear_result = base_fields.Float() 
    classify_result = base_fields.String() 
    metric = base_fields.Float() 
    class Meta:
        pass

class IrisFigureSchema(ModelSchema):
    """
    IRIS pager schema
    """
    figure_name = base_fields.String() 
    class Meta:
        pass