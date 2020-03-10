"""

Notice Content Module Request Parameter

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters
from .schema import *
from app.common.param import PagerParameters

class Notice_contentParameters(JSONParameters, Notice_contentSchema):
    """
    Notice Content Parameters
    """
    class Meta(Notice_contentSchema.Meta):
        pass

class ExtendPagerParameters(PagerParameters):
    receiver = base_fields.Integer(required=False)

class ReadStatusParameters(JSONParameters):
    id = base_fields.Integer(required=True)
    status = base_fields.Boolean(required=True)