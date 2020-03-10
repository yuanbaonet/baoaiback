"""
notice_content and admin relation module database models

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app import db
from app.common.mixin import * 

class Notice_contentAdmin(TableMixin, db.Model):
    __tablename__ = 'notice_content_admin'
    notice_content_id = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('notice_content_id', 'admin_id', name='uix_notice_content_admin_notice_content_id_admin_id'),
    )
    
    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "title=\"{self.title}\""
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )









