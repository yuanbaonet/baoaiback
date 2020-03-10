"""
IRIS module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
"""

from app.api import api

def init_app(app, **kwargs):
    """
    Init IRIS module.
    """
    from . import resource
    api.add_namespace(resource.ns)