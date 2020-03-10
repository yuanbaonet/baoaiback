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

class Attachments(TableMixin, db.Model):
    __tablename__ = 'attachments'
    admin_id = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, nullable=False, default=0)
    module_name = db.Column(db.String(100), nullable=False, default='attachments') # Module Name
    module_obj_id = db.Column(db.Integer, nullable=False, default=0) # Module Object ID
    url = db.Column(db.String(255), nullable=False)
    uuid = db.Column(db.String(100), nullable=False)
    imagewidth = db.Column(db.String(30), nullable=False, default="0")
    imageheight = db.Column(db.String(30), nullable=False, default="0")
    imagetype = db.Column(db.String(30), nullable=True)   
    imageframes = db.Column(db.Integer, nullable=False, default=0)
    filesize = db.Column(db.Integer, nullable=False, default=0)
    mimetype = db.Column(db.String(100), nullable=True)
    isimage = db.Column(db.Boolean(), nullable=False, default=True) # is image, 1/True: Image  0/False: File
    iscover = db.Column(db.Boolean(), nullable=False, default=False) # is cover, 1/True: cover  0/False: not cover
    weight = db.Column(db.Integer, nullable=False, default=0)
    extparam = db.Column(db.String(255), nullable=True)
    storage = db.Column(db.String(100), nullable=False, default="local")
    sha1 = db.Column(db.String(40), nullable=True)
    md5 = db.Column(db.String(40), nullable=True)
    category_id = db.Column(db.Integer, nullable=False, default=0)
    category_main = db.Column(db.String(100), nullable=False, index=True, default='uncategorized')
    category_sub = db.Column(db.String(100), nullable=False, index=True, default='uncategorized')

    def __repr__(self):
        return '<Attachments %r>' % self.title





