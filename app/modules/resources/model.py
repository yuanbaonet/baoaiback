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

class Resources(TableMixin, db.Model):
    __tablename__ = 'resources'
    pid = db.Column(db.Integer, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(128), nullable=False, default='fa fa-circle-o')
    remark = db.Column(db.String(255), nullable=True)
    ismenu = db.Column(db.Boolean, nullable=False, default=True) # is menu  1 menu 0 feature 
    weight = db.Column(db.Integer, nullable=False, default=0) # weight , Used for sorting，Descending order
    method = db.Column(db.String(20), nullable=False, default='GET')  # Routing access method, value: GET POST DELETE PUT OPTION
    name = db.Column(db.String(50), nullable=False, unique=True)
    link_type = db.Column(db.String(30), nullable=True, unique=False, index=False)
    '''
    Writing of ui-sref transfer parameters:
    ui-sref = "page ({parameter 1: parameter 1 value, parameter 2: parameter 2 value,... })"
    
    For example:
    {module_id:0}
    '''
    params =  db.Column(db.String(255), nullable=True)
    locked = db.Column(db.Boolean(), nullable=False, default=False)
    # tree
    treepath = db.Column(db.String(255), nullable=True) # tree path, for example: .2.120. , 0 does not need to be at the front
    treegrade = db.Column(db.Integer, nullable=True) # Tree depth, top level is 0, .2.120. is 2
    treepathweight = db.Column(db.String(255), nullable=True) # tree path weight, for example: 2000.2.1500.120. , The weight of node id = 2 is 2000,  The weight of node id = 120 is 1500
    





