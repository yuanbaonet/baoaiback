"""result

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from flask import current_app,request
from .status import Status
class Result(object):
    @staticmethod
    def success(data={}, status=Status.SUCCESS.status, message=Status.SUCCESS.message):
        ret_json = {
            "status": status,
            "message": message,
            "data": data
        }
        return ret_json

    @staticmethod
    def error(data={}, status=Status.ERROR.status, message=Status.ERROR.message):
        ret_json = {
            "status": status,
            "message": message,
            "data": data
        }
        return ret_json        
