"""param

Request Parameter

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
from flask_marshmallow import base_fields
from marshmallow import validate, ValidationError
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters
from .schema import *

def validate_length(value):
    if len(value) < 3 or len(value) > 30:
        raise ValidationError('Length [3-30]')

class AdminLoginParameters(JSONParameters):
    username = base_fields.String(required=True, validate=validate_length)
    password = base_fields.String(required=True)

class AdminParameters(JSONParameters, AdminSchema):
    class Meta(AdminSchema.Meta):
        pass

class FindPassParameters(JSONParameters):
    email = base_fields.String(required=True, validate=validate.Email(error='Format Error'))

class RefleshTokenParameters(JSONParameters):
    rftoken = base_fields.String(required=True)
    username = base_fields.String(required=True)

class UidsRidsParameters(JSONParameters):
    rids = base_fields.List(base_fields.Integer()) 
    uids = base_fields.List(base_fields.Integer()) 

