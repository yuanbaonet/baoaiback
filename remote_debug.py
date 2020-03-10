"""remote_debug

Remote Debug Main File For Visual Studio Code
仅用于Visual Studio Code的远程调试入口文件

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
import os
from app import create_app, db

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    app.debug = False
    app.run(host='localhost', port=5002)