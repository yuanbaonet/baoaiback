"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
from app import db, Config
from .model import Admin
from app.common.status import Status 
import random
import string
from datetime import datetime, timedelta
from collections import OrderedDict
from app.common.mail import mail
from app.modules.adminroles.model import AdminRoles
from app.modules.roles.model import Roles
import logging

# logger = logging.getLogger("dao")
# logger.debug('admin dao')

class AdminDao(object):
    def delete(self, ids):
        """delete

        delete condition: id list

        Args:
            ids (list): id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            for id in ids :
                locked = self.locked(id)
                if locked :
                    raise Exception('object(id=%s) is locked'%(id))
            try:
                Admin.query.filter(Admin.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def deleteByUsername(self, username):
        """delete

        delete condition: username
        
        Args:
            username (str): username
            
        Returns:
            bool: True or False

        """
        result = False
        if username:
            try:
                Admin.query.filter(Admin.username == username).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def add(self, args):
        """add

        add condition: username or email must be unique, password is encrypted.
        用户名和email必须是唯一，密码hash加密保存

        Args:
            args (collections.OrderedDict): args
            
        Returns:
            object: Admin object

        """
        record = None
        username = args.get('username')
        email = args.get('email')
        DEFAULT_ADMIN = Config.DEFAULT_ADMIN      
        if Admin.query.filter_by(username=username).first() :
            raise Exception('Account Exists')
        if Admin.query.filter_by(email=email).first() :
            raise Exception('Email Exists')
        try:
            record = Admin(**args)
            record.password = args.pop('password_hash')
            db.session.add(record)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        if record :
            uids = []
            rids = []
            uids.append(record.id)
            rids.append(DEFAULT_ADMIN)
            try:
                self.addAdminRoles(uids, rids)
            except Exception as e:
                pass
        return record

    def edit(self, args):
        """edit

        Args:
            args (collections.OrderedDict): args
            
        Returns:
            object: Admin object

        """
        id = args.pop('id')
        record = Admin.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    if k == 'password_hash':
                        if v :
                            setattr(record,'password',v)
                    else:
                        setattr(record,k,v)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def getById(self, id):
        """view

        view condition: id

        Args:
            id (int): id
            
        Returns:
            object: Admin object

        """
        record = Admin.query.get(id)
        return record

    def getByUsername(self, username):
        """view

        view condition: username

        Args:
            username (str): username
            
        Returns:
            object: Admin object

        """
        record = Admin.query.filter(Admin.username==username).first()
        return record

    def getList(self, search, sort, order, offset, limit):
        """List

        list condition: pagination

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        if search.strip() != '' :
            temp_query_obj = Admin.query.filter(or_(Admin.username.like("%{search}%".format(search=search)), Admin.email.like("%{search}%".format(search=search))))
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Admin.query.order_by(eval("Admin."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Admin."+sort+"."+order+"()"))
        if temp_query_obj == None :
            pages = Admin.query.paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getUserByToken(self, token):
        """Get user info by token. # 由令牌得到用户信息

        Token contains user's id, username and timestamp, get user info by id.

        Args:
            token (str): token string
            
        Returns:
            object: Admin object

        """
        user = None
        data = {}
        if token:
            data = Admin.confirm(token)
            if data.get('status') == Status.TOKEN_SUCCESS.status:
                        uid = data['data']['id']
                        user = Admin.query.get(uid)
        return user

    @staticmethod
    def getRandomNumKey(num):
        """Randomly generated new password.  # 随机产生新密码

        Randomly generated num-digit passwords containing a-z, A-Z, 0-9

        Args:
            num (int): password length is num
            
        Returns:
            str: new random password

        """
        a=string.ascii_letters+string.digits # 数据源是a-z,A-Z，0-9
        key=random.sample(a,num)
        keys="".join(key)
        return keys

    def findPass(self, receiver):
        """Retrieve the password with email. # 使用邮件找回密码

        Args:
            receiver (str): receiver email
            
        Returns:
            bool: True or False

        """
        result = False
        admin = Admin.query.filter_by(email=receiver).first()
        if not admin :
            raise Exception("Email does not exist")
        new_password = AdminDao.getRandomNumKey(8)
        sender = Config.MAIL_SENDER
        sender_pass = Config.MAIL_SENDER_PASS
        mail_message = Config.MAIL_MESSAGE + new_password
        mail_message_fail = Config.MAIL_MESSAGE_FAIL
        mail_subject = Config.MAIL_SUBJECT
        from_ = Config.MAIL_FROM
        send_res = mail(sender, sender_pass, receiver, from_, receiver, mail_subject, mail_message) 
        if send_res['status'] :
            try:
                admin.password = new_password
                db.session.add(admin)
                db.session.commit()
                result = True
            except Exception as e:
                db.session.rollback()
                send_res = mail(sender, sender_pass, receiver, from_, receiver, mail_subject, mail_message_fail) 
                raise Exception(mail_message_fail)
        return result

    def login(self, username, password):
        """Login # 登录

        If the password is entered incorrectly 5 times , wait for 1 minute before verification.
        如果连续错误录入5次密码（login_failure字段记录），强行等待1分钟（当前和updated时间差与间隔一分钟 timedelta(minutes=1)比较）后才能验证。

        Args:
            username (str): username
            password (str): password
            
        Returns:
            object: For example: {'token': token, 'rftoken': rftoken, 'nickname': user.nickname, 'username': user.username, 'avatar': user.avatar, 'id': user.id, 'title': user.title}

        """
        isVerify = True # 是否可以密码验证，如果连续错误录入5次密码，强行等待1分钟后才能验证。
        isExcept = False # 是否异常
        data = {}
        user = Admin.query.filter_by(username=username).first()
        if user and password:
            login_failure = user.login_failure + 1
            if login_failure >5 :
                isVerify = False
                updated = user.updated
                curr = datetime.now()
                dist = curr - updated
                step_period = timedelta(minutes=1)
                if dist > step_period:
                    isVerify = True
                    login_failure = 0
            if isVerify :
                ret = user.verify_password(password)
                if ret:
                    token = user.generate_token(Config.TOKEN_EXPIRES)
                    rftoken = user.generate_token(Config.REFRESH_TOKEN_EXPIRES)
                    data = {'token': token, 'rftoken': rftoken, 'nickname': user.nickname, 'username': user.username, 'avatar': user.avatar, 'id': user.id, 'title': user.title}
                    login_failure = 0
                else :
                    isExcept = True
                new_args = OrderedDict()
                new_args['id'] = user.id
                new_args['login_failure'] = login_failure
                self.edit(new_args)
            else :
                raise Exception("Account or Password Error, Wait 60 Seconds")
        else :
            isExcept = True
        if isExcept :
            raise Exception("Account or Password Error")
        return data

    def reflesh_token(self, rftoken, username):
        """Reflesh Token # 更新令牌

        Args:
            rftoken (str): reflesh token
            username (str): username
            
        Returns:
            object: For example: {'token': token}

        """
        data = {}
        user = Admin.query.filter(Admin.username==username).first()
        if user :
            token = user.generate_new_token(Config.TOKEN_EXPIRES, username, rftoken)
            if token :
                data = {'token': token}
            else :
                raise Exception("Token Generate Fail")
        else :
            raise Exception("Account Error")
        return data

    def addAdminRoles(self, uids, rids):
        """Add admin and roles relationships # 增加用户和角色关系

        add condition: rids and uids

        Args:
            uids (list): user id list
            rids (list): roles id list            
            
        Returns:
            bool: True or False

        """
        result = False
        if rids and uids :
            try:
                AdminRoles.query.filter(AdminRoles.uid.in_(tuple(uids))).delete(synchronize_session=False)
                db.session.flush()
                for rid in rids :
                    for uid in uids :
                        adminRoles = AdminRoles(uid=uid, rid=rid)
                        db.session.add(adminRoles)
                        db.session.flush()
                db.session.commit()
                result = True
            except Exception as e :
                db.session.rollback()
                raise Exception(e)
        return result

    def getRBAC(self, uid):
        """Get RBAC with user id. # 通过User ID获取基于角色的权限信息

        by user id, get user's roles and resources

        Args:
            uid (int): user id
            
        Returns:
            object: RolesDetailSchema

        """
        rolesDetail = {}
        rids = []
        rids_str = ''
        role_titles = []
        role_titles_str = ''
        resources_ids = []
        resources_ids_str = ''
        resources_ids_set = set()
        try:
            roles = db.session.query(Roles.id.label('rid') , Roles.title.label('title'), Roles.resources.label('resources')). \
                filter(Roles.status == 1). \
                filter(Roles.id == AdminRoles.rid). \
                filter(AdminRoles.uid == uid). \
                order_by(Roles.weight.desc()). \
                all()   
            if roles :
                for role in roles :
                    rids.append(role.rid)
                    role_titles.append(role.title)
                    resources_ids_set = resources_ids_set | eval('{'+role.resources+'}')
                rolesDetail['uid'] = uid
                rolesDetail['rids'] = rids
                rolesDetail['rids_str'] = str(rids)[1:len(str(rids))-1]
                rolesDetail['titles'] = str(role_titles)[1:len(str(role_titles))-1]
                rolesDetail['resources_ids'] = list(resources_ids_set)
                rolesDetail['resources_ids_str'] = str(list(resources_ids_set))[1:len(str(list(resources_ids_set)))-1]
                rolesDetail['roles'] = roles
        except Exception as e :
            raise Exception(e)
        return rolesDetail

    def locked(self, id):
        """is locked # 是否锁定

        Args:
            id (int): id
            
        Returns:
            bool: True or False

        """
        result = False
        # Get module info
        record = self.getById(id)  
        if not record:
             raise Exception('object(id=%s) is null'%id)
        if record.locked == 1 :
            result = True
        return result
