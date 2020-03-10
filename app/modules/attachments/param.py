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
from flask_restplus_patched import JSONParameters, Parameters, PostFormParameters
from .schema import *
from app.common.param import PagerParameters

class AttachmentsParameters(JSONParameters, AttachmentsSchema):
    class Meta(AttachmentsSchema.Meta):
        pass

class ExtendPagerParameters(PagerParameters):
    module_name = base_fields.String(required=False)
    module_obj_id = base_fields.Integer(required=False)
    category_id = base_fields.Integer(required=False)

class CEditorFileBrowserUploadParameters(PostFormParameters):
    CKEditorFuncNum = base_fields.Integer(required=False)
    CKEditor = base_fields.String(required=False)
    langCode = base_fields.String(required=False)
    ckCsrfToken = base_fields.String(required=False)

class RemoteImgURLParameters(Parameters):
    remote_img_url = base_fields.String(required=False)