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

class AttachmentsSchema(ModelSchema):
    class Meta:
        model = Attachments

class AttachmentsListPagerSchema(ModelSchema):
    total = base_fields.Integer() 
    rows = base_fields.Nested(AttachmentsSchema, many=True)
    class Meta:
        pass

class CKeditorUploadErrorSchema(ModelSchema):
    message = base_fields.String() 
    class Meta:
        pass
    
class AttachmentsCKeditorUploadSchema(ModelSchema):
    uploaded = base_fields.Integer() 
    fileName = base_fields.String()
    url = base_fields.String()
    error = base_fields.Nested(CKeditorUploadErrorSchema)
    class Meta:
        pass



