"""param

Request Parameter

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters
from .schema import *

class RolesParameters(JSONParameters, RolesSchema):
    class Meta(RolesSchema.Meta):
        pass
