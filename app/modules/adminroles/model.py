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

class AdminRoles(TableMixin, db.Model):
    __tablename__ = 'admin_roles'
    uid = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('uid', 'rid', name='uix_admin_roles_uid_rid'),
    )
    
    def __repr__(self):
        return '<AdminRoles id:%r, uid:%r, rid:%r>' % (self.id, self.uid, self.rid)





