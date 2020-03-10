"""
IRIS database models

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
"""

from app import db
from sqlalchemy.schema import FetchedValue
from app.common.mixin import * 

class Iris(PureTableMixin, db.Model):
    """
    IRIS database model.
    """   
    __tablename__ = 'iris'    
    sepal_length = db.Column(db.Float(), nullable=True, unique=False, index=False)
    sepal_width = db.Column(db.Float(), nullable=True, unique=False, index=False)
    petal_length = db.Column(db.Float(), nullable=True, unique=False, index=False)
    petal_width = db.Column(db.Float(), nullable=True, unique=False, index=False)
    irisclass = db.Column(db.String(30), nullable=True, unique=False, index=False)        
   
    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
