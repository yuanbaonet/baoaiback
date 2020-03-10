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

class Logs(TableMixin, db.Model):
    """Model Class"""
    __tablename__ = 'logs'
    uid = db.Column(db.Integer, index=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)
    method = db.Column(db.String(10), nullable=True)
    referer = db.Column(db.String(255), nullable=True)
    path  = db.Column(db.String(255), nullable=True)
    base_path  = db.Column(db.String(255), nullable=True)
    route  = db.Column(db.String(100), nullable=True)
    ip = db.Column(db.String(32), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    desc = db.Column(db.Text(), nullable=True)
    
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









