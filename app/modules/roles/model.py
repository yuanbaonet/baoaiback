"""model

Database Table Model

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from app.common.mixin import * 

class Roles(TableMixin, db.Model):
    __tablename__ = 'roles'
    pid = db.Column(db.Integer, nullable=False)
    resources = db.Column(db.Text, nullable=False)
    remark = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Integer, nullable=False, default=0) # Weight determines order, inverse order
    locked = db.Column(db.Boolean(), nullable=False, default=False)
    # tree
    treepath = db.Column(db.String(255), nullable=True) # tree path, for example: .2.120. , 0 does not need to be at the front
    treegrade = db.Column(db.Integer, nullable=True) # Tree depth, top level is 0, .2.120. is 2
    treepathweight = db.Column(db.String(255), nullable=True) # tree path weight, for example: 2000.2.1500.120. , The weight of node id = 2 is 2000,  The weight of node id = 120 is 1500





