"""
RESTful API notice_content and admin relation module resource

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app import db
from flask import current_app,request
from app.common.status import Status
from app.common.schema import *
from app.common.param import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from app.common.result import Result
from .model import *
from .schema import *
from .param import *
from sqlalchemy import or_

ns = Namespace("Notice_contentAdmin", description="RESTful API Notice_contentAdmin resource")
