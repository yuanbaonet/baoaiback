"""

Category Module Request Parameter

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-04 10:04:19
"""

from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters
from .schema import *
from app.common.param import PagerParameters

class CategoryParameters(JSONParameters, CategorySchema):
    """
    Category Parameters
    """
    class Meta(CategorySchema.Meta):
        pass

class ExtendPagerParameters(PagerParameters):
    articles = base_fields.Integer(required=False)
    books_category_id = base_fields.Integer(required=False)
    nav_category_id = base_fields.Integer(required=False)
    is_book = base_fields.Boolean(required=False)
    is_main = base_fields.Boolean(required=False)

class NewsExtendPagerParameters(PagerParameters):
    articles = base_fields.Integer(required=False)
    news_category_id = base_fields.Integer(required=False)

class FieldParameters(Parameters):
    category = base_fields.Integer(required=False)
    field = base_fields.String(required=False)

