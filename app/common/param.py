"""param

Request Parameter
请求参数

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from flask_marshmallow import base_fields
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters

class BasicPagerParameters(Parameters):
    page = base_fields.Integer(required=True)
    limit = base_fields.Integer(required=True)

class PagerParameters(Parameters):
    search = base_fields.String(required=False, default='')
    sort = base_fields.String(required=False, default='')
    order = base_fields.String(required=True, default='asc')
    offset = base_fields.Integer(required=True, default=0)
    limit = base_fields.Integer(required=True, default=10)
    lang = base_fields.String(required=False, default='')

class PagerJSONParameters(JSONParameters):
    search = base_fields.String(required=False, default='')
    sort = base_fields.String(required=False, default='')
    order = base_fields.String(required=True, default='asc')
    offset = base_fields.Integer(required=True, default=0)
    limit = base_fields.Integer(required=True, default=10)
    lang = base_fields.String(required=False, default='')

class IDSParameters(JSONParameters):
    ids = base_fields.List(base_fields.Integer()) 

class IDJSONParameters(JSONParameters):
    id = base_fields.Integer(required=True)

class UIDParameters(Parameters):
    """
    Uniform ID
    """
    uid = base_fields.Integer(required=True)

class IDParameters(Parameters):
    """
    ID
    """
    id = base_fields.Integer(required=True)

class UIDAndIDSParameters(JSONParameters):
    """
    UID And IDS
    """
    uid = base_fields.Integer(required=True)
    ids = base_fields.List(base_fields.Integer()) 

class LangParameters(Parameters):
    lang = base_fields.String(required=False)