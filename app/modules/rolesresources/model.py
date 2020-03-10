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

class RolesResources(TableMixin, db.Model):
    __tablename__ = 'roles_resources'
    rid = db.Column(db.Integer, nullable=False)
    reid = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('rid', 'reid', name='uix_roles_resources_rid_reid'),
    )
    
    def __repr__(self):
        return '<RolesResources %r>' % self.title










