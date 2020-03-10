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
from app.common.schema import BasicSchema,BasicPagerSchema
from .model import *

class AdminSchema(ModelSchema):
    """
    Base Admin schema exposes only the most general fields.
    """
    class Meta:
        model = Admin

class AdminListPagerSchema(ModelSchema):
    total = base_fields.Integer() 
    rows = base_fields.Nested(AdminSchema(exclude=['password_hash']), many=True)
    class Meta:
        pass

class RolesSchema(ModelSchema):
    rid = base_fields.Integer()
    title = base_fields.String()
    resources = base_fields.String()
    class Meta:
        pass

class RolesDetailSchema(ModelSchema):
    uid = base_fields.Integer()
    rids = base_fields.List(base_fields.Integer())
    rids_str = base_fields.String()
    resources_ids = base_fields.List(base_fields.Integer()) 
    resources_ids_str = base_fields.String()
    titles = base_fields.String()
    roles = base_fields.Nested(RolesSchema, many=True)
    class Meta:
        pass








