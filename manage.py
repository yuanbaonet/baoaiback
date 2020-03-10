"""manage

BaoAI Backend Main File

PROJECT: BaoAI Backend
VERSION: 2.0.0
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server, Command
from flask_script.commands import Clean, ShowUrls
from app import create_app, db

# app,celery = create_app() 
app = create_app()
manager = Manager(app)  
migrate = Migrate(app, db)

def make_shell_context():
    from app.modules.admin.model import Admin
    return dict(app=app, db=db, Admin=Admin)

# Get BaoAI version and URL # 获取BaoAI版本及官方URL
@manager.command  
def baoai():  
    print('BaoAI v2.0.0 - http://www.baoai.co')

manager.add_command("runserver", Server(host='0.0.0.0', port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)  # Database Manage # 数据库管理
manager.add_command("clean", Clean())  # Clean Cache File # 清理缓存文件
manager.add_command("url", ShowUrls())  # Print All URL # 打印所有URL

if __name__ == "__main__":  
    manager.run()  




