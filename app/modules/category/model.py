"""
Category database models

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-04 10:04:19
"""

from app import db
from sqlalchemy.schema import FetchedValue
from app.common.mixin import * 

class Category(TableMixin, db.Model):
    """
    Category database model.
    """   
    __tablename__ = 'category'    
    ismenu = db.Column(db.Boolean(), nullable=True, unique=False, index=False, default='True')
    pid = db.Column(db.Integer(), nullable=False, unique=False, index=True, default='0')
    title = db.Column(db.String(255), nullable=False, unique=False, index=True)
    alias = db.Column(db.String(100), nullable=True, unique=False, index=False)
    weight = db.Column(db.Integer(), nullable=False, unique=False, index=True, default='0')
    keywords = db.Column(db.String(255), nullable=True, unique=False, index=False)
    summary = db.Column(db.Text(), nullable=True, unique=False, index=False)
    content = db.Column(db.Text(), nullable=True, unique=False, index=False)
    link_type = db.Column(db.String(30), nullable=True, unique=False, index=False)
    inner_link = db.Column(db.Integer(), nullable=True, unique=False, index=False, default='0')
    link_target = db.Column(db.String(255), nullable=True, unique=False, index=False, default='_blank')
    link = db.Column(db.String(255), nullable=True, unique=False, index=False)
    block_link = db.Column(db.Integer(), nullable=True, unique=False, index=False)
    article_link = db.Column(db.Integer(), nullable=True, unique=False, index=False)
    articles = db.Column(db.Integer(), nullable=True, unique=False, index=False)
    route_link = db.Column(db.String(255), nullable=True, unique=False, index=False)
    cover = db.Column(db.String(255), nullable=True, unique=False, index=False)
    views = db.Column(db.Integer(), nullable=True, unique=False, index=False, default='0')
    # tree
    treepath = db.Column(db.String(255), nullable=True) # tree path, for example: .2.120. , 0 does not need to be at the front # 树路径
    treegrade = db.Column(db.Integer, nullable=True) # Tree depth, top level is 0, .2.120. is 2 # 树深度
    # tree path weight, Weight for tree sort. for example: 2000.2.1500.120. , The weight of node（id = 2） is 2000,  The weight of node（id = 120） is 1500 
    # 树路径权重，用于树形排序。如：2000.2.1500.120. , 结点ID是2 的权重是2000 ， 结点ID是120的权重是1500
    treepathweight = db.Column(db.String(255), nullable=True)        
   
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
