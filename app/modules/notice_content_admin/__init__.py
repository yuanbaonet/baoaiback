"""
notice_content and admin relation module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app.api import api
def init_app(app, **kwargs):
    """
    Init notice_content_admin module.
    """
    from . import resource
    api.add_namespace(resource.ns)