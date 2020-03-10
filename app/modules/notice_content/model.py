"""
Notice Content database models

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app import db
from sqlalchemy.schema import FetchedValue
from app.common.mixin import * 

class Notice_content(TableMixin, db.Model):
    """
    Notice Content database model.
    """   
    __tablename__ = 'notice_content'
    
    title = db.Column(db.String(255), nullable=False, unique=False, index=True)
    icon = db.Column(db.String(100), nullable=True, unique=False, index=False, default='fa fa-circle-o')
    content = db.Column(db.Text(), nullable=True, unique=False, index=False)
    receiver = db.Column(db.Integer(), nullable=True, unique=False, index=False)
    module = db.Column(db.String(100), nullable=True, unique=False, index=False)
    reference = db.Column(db.String(255), nullable=True, unique=False, index=False)
    reference_params = db.Column(db.String(255), nullable=True, unique=False, index=False)
    status = db.Column(db.Boolean(), nullable=False, unique=False, index=True, default=True)
    weight = db.Column(db.Integer(), nullable=True, unique=False, index=False, default='0')
    
    
   
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
