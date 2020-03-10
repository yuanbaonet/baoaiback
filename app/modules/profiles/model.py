from app import db
from app.common.mixin import * 

class Profiles(TableMixin, db.Model):
    """Model Class"""
    __tablename__ = 'profiles'
    uid = db.Column(db.Integer, unique=True, index=True, nullable=False)
    career = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    postcode  = db.Column(db.String(32), nullable=True)
    mobilephone  = db.Column(db.String(32), nullable=True)
    tel  = db.Column(db.String(32), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    motto = db.Column(db.String(255), nullable=True)
    firstname = db.Column(db.String(32), nullable=True)
    lastname = db.Column(db.String(32), nullable=True)
    qq = db.Column(db.String(16), nullable=True)
    weixin = db.Column(db.String(32), nullable=True)
    weibo = db.Column(db.String(32), nullable=True)
    idnumber = db.Column(db.String(18), nullable=True)
    birthday = db.Column(db.Date(), nullable=True)
    email_notice = db.Column(db.Boolean(), nullable=True, default=False)
    sms_notice = db.Column(db.Boolean(), nullable=True, default=False)
    weixin_notice = db.Column(db.Boolean(), nullable=True, default=False)
    
    def __repr__(self):
        """Class Serialization"""
        return '<Profiles %r>' % self.uid










