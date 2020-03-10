"""profiles

Init profiles module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app.api import api
def init_app(app, **kwargs):
    """
    Init profiles module.
    """
    from . import resource
    api.add_namespace(resource.ns)