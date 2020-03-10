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

class Configs(TableMixin, db.Model):
    """Model Class"""
    __tablename__ = 'configs'
    uid = db.Column(db.Integer, nullable=False)
    module = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(100), nullable=False)
    keys = db.Column(db.String(100), nullable=False)
    value  = db.Column(db.Text(), nullable=True)
    __table_args__ = (
        db.UniqueConstraint('module', 'section', 'keys', 'lang', name='uix_configs_module_section_keys_lang'),
    )
    
    def __repr__(self):
        """Class Serialization"""
        return '<Configs %r>' % (self.module + '.' + self.section + '.' + self.key + '.' + self.lang + ' = ' + self.value)










