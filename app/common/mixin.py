"""mixin

Model predefinition

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import Config, db
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

class TableMixin: 
    '''Data table object, global settings set public properties and methods # 数据表对象， 全局设置设置公共属性与方法
    '''
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=False, default=0) # parent id # 父ID
    title = db.Column(db.String(255), nullable=True)   
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.now) # 记录增加时间
        #db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(
        db.DateTime, onupdate=datetime.now) # 记录修改时间
        #db.DateTime, onupdate=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=True, index=True) # Record status True/1=normal False/0=pause # 记录状态， 1 正常 0 暂停
    weight = db.Column(db.Integer, nullable=False, default=0, index=True) # Weight, the higher the value, the higher the order # 权重，值越大排序越前
    lang = db.Column(db.String(10), nullable=False, index=True,  default='all') # lang: all zh-cn zh-tw en jp kr
    uid = db.Column(db.Integer, nullable=False, default=0, index=True) # admin or user id # 用户ID

    @declared_attr 
    def __tablename__(cls): 
        _table_prefix = Config.TABLE_PREFIX
        return _table_prefix + cls.__name__.lower() 

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

class PureTableMixin: 
    id = db.Column(db.Integer, primary_key=True)
    
    @declared_attr 
    def __tablename__(cls): 
        _table_prefix = Config.TABLE_PREFIX
        return _table_prefix + cls.__name__.lower() 

class StockTableMixin: 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)   

class StockPureTableMixin: 
    id = db.Column(db.Integer, primary_key=True)


