"""configs

Init task module

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
from www import celery
from celery.schedules import crontab

@celery.task
def test1(arg1, arg2):
    result = arg1 + arg2
    return result

@celery.task
def test2(arg):
    print(arg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test2.s('Happy Mondays!'),
    )

