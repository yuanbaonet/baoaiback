"""schema

Notice Content Module Response Schema

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from flask_restplus_patched import ModelSchema
from flask_marshmallow import base_fields
from .model import *

class Notice_contentSchema(ModelSchema):
    """
    Notice Content schema
    """
    receive_created = base_fields.DateTime()
    receive_id = base_fields.Integer()
    class Meta:
        model = Notice_content

class Notice_contentListPagerSchema(Notice_contentSchema):
    """
    Notice Content pager schema
    """
    total = base_fields.Integer() 
    rows = base_fields.Nested(Notice_contentSchema, many=True)
    class Meta:
        pass