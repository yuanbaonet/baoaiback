"""

Notice Content Module Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app import db
from .model import *
from flask import current_app
from sqlalchemy import or_, func
from collections import OrderedDict
from app.modules.notice_content_admin.model import *
from app.modules.admin.model import *
from ..notice_content_admin.dao import *


class Notice_contentDao(object):
    def delete(self, ids):
        """delete

        Args:
            ids (list): id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Notice_content.query.filter(Notice_content.id.in_(tuple(ids))).delete(synchronize_session=False)
                Notice_contentAdmin.query.filter(Notice_contentAdmin.notice_content_id.in_(tuple(ids))).delete(synchronize_session=False)
                
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def add(self, args):
        """add

        Args:
            args (OrderedDict): form args
            
        Returns:
            object: Notice_content object

        """
        record = None
        try:
            record = Notice_content(**args)
            db.session.add(record)
            
            receiver = record.receiver
            if receiver :
                new_args = OrderedDict()
                new_args['notice_content_id'] = id
                new_args['admin_id'] = receiver
                new_record = Notice_contentAdmin(**new_args)
                db.session.add(new_record)
                db.session.flush()
                
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return record

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Notice_content object

        """
        id = args.pop('id')
        record = Notice_content.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
                
                receiver = record.receiver
                if receiver :
                    notice_contentAdmin = Notice_contentAdmin.query.filter(Notice_contentAdmin.notice_content_id==receiver, Notice_contentAdmin.admin_id==id).first()
                    if not notice_contentAdmin :
                        new_args = OrderedDict()
                        new_args['notice_content_id'] = id
                        new_args['admin_id'] = receiver
                        new_record = Notice_contentAdmin(**new_args)
                        db.session.add(new_record)
                        db.session.flush()                        
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def getById(self, id):
        """view by id

        Args:
            id (int): id
            
        Returns:
            object: Notice_content object

        """
        record = Notice_content.query.get(id)
        return record

    def getList(self, search, sort, order, offset, limit):
        """view list

        condition: pagination

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            
        Returns:
            object: data, for example: {"rows": lst, "total":total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        total = 0
        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Notice_content.query.filter(Notice_content.id.in_(ids)).offset(offset).limit(limit).all()
            total = db.session.query(func.count(Notice_content.id)).filter(Notice_content.id.in_(ids)).offset(offset).limit(limit).scalar() 
            if pages:
                for item in pages:
                    lst.append(item)
                data =  {"rows": lst, "total":total}
            return data
        temp_query_obj = Notice_content.query
        total_query_obj = db.session.query(func.count(Notice_content.id))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
            total_query_obj = total_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
            total_query_obj = total_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '' :
            pages = temp_query_obj.order_by(Notice_content.created.desc()).offset(offset).limit(limit).all()
        else :
            pages = temp_query_obj.offset(offset).limit(limit).all()
        total = total_query_obj.scalar() 
        if pages:
            for item in pages:
                lst.append(item)
            data =  {"rows": lst, "total":total}
        return data

    def getListByLang(self, search, sort, order, offset, limit, lang):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        total = 0
        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Notice_content.query.filter(Notice_content.id.in_(ids)).filter(Notice_content.lang.in_((lang, 'all'))).offset(offset).limit(limit).all()
            total = db.session.query(func.count(Notice_content.id)).filter(Notice_content.id.in_(ids)).filter(Notice_content.lang.in_((lang, 'all'))).offset(offset).limit(limit).scalar() 
            if pages:
                for item in pages:
                    lst.append(item)
                data =  {"rows": lst, "total":total}
            return data
        temp_query_obj = Notice_content.query
        total_query_obj = db.session.query(func.count(Notice_content.id))
        if lang.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Notice_content.lang.in_((lang, 'all')))
            total_query_obj = total_query_obj.filter(Notice_content.lang.in_((lang, 'all')))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
            total_query_obj = total_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
            total_query_obj = total_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '' :
            pages = temp_query_obj.order_by(Notice_content.created.desc()).offset(offset).limit(limit).all()
        else :
            pages = temp_query_obj.offset(offset).limit(limit).all()
        total = total_query_obj.scalar() 
        if pages:
            for item in pages:
                lst.append(item)
            data =  {"rows": lst, "total":total}
        return data

    def getListByLangAndReceiver(self, search, sort, order, offset, limit, lang, receiver):
            """notification list related to a recipient # 查询某接收者相关的通知列表

            condition: pagination by lang

            Args:
                search (str): search field, default is title field
                sort (str): sort field
                order (str): order type (asc/desc), default is asc
                offset (int): Paging offset
                limit (int): Maximum number of records per page
                lang (str): language
                receiver (int): refer to admin's id
                
            Returns:
                object: data, for example: {"rows": lst, "total":pages.total}

            """
            data = {}
            page = offset // limit + 1
            temp_query_obj = None
            pages = None
            lst = []
            if search.startswith( 'id=' ) and len(search)>3 :
                ids = search[3:]
                ids = eval('['+ids+']')
                pages = Notice_content.query.filter(Notice_content.id.in_(ids)).filter(Notice_content.lang.in_((lang, 'all'))).paginate(page, limit)
                if pages:
                    for item in pages.items:
                        lst.append(item)
                    data =  {"rows": lst, "total":pages.total}
                return data
            if not receiver :
                return self.getListByLang(search, sort, order, offset, limit, lang)
            temp_query_obj = db.session.query(Notice_content)
            if lang.strip() != '' :
                temp_query_obj = temp_query_obj.filter(Notice_content.lang.in_((lang, 'all')))
            if search.strip() != '' :
                temp_query_obj = temp_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                temp_query_obj = temp_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = temp_query_obj.filter(Notice_content.id == Notice_contentAdmin.notice_content_id).filter(Notice_contentAdmin.admin_id == receiver).order_by(Notice_content.treepathweight.asc()).paginate(page, limit)
            else :
                pages = temp_query_obj.filter(Notice_content.id == Notice_contentAdmin.notice_content_id).filter(Notice_contentAdmin.admin_id == receiver).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data                    

    def addAdmin(self, id, admin_ids):
        """Add Admin id To Notice_contentAdmin # 增加需要通知的账号

        Args:
            id (id): notice content id # 通知内容ID
            admin_ids (list): managers list # 需要通知的管理员或用户列表                    
            
        Returns:
            object: Last associated record #最后关联记录
        """
        record = None
        try:
            args = OrderedDict()
            for admin_id in admin_ids :
                args['notice_content_id'] = id
                args['admin_id'] = admin_id
                record = Notice_contentAdmin(**args)
                db.session.add(record)
                db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return record

    def deleteAdmin(self, id, ids):
        """Delete the associated record of user and notification conten # 删除用户和通知内容的关联记录

        Args:
            id (int): notice_content id # 通知内容ID
            ids (list): admin id list # 与通知关联用户ID列表
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Notice_contentAdmin.query.filter(Notice_contentAdmin.notice_content_id==id).filter(Notice_contentAdmin.admin_id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def deleteAdminAll(self, ids):
        """Delete all records in the Notice_contentAdmin table associated with the content ID # 删除与内容ID有关联的所有Notice_contentAdmin表中记录

        Args:
            ids (int): notice_content id list # 内容ID列表
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Notice_contentAdmin.query.filter(Notice_contentAdmin.notice_content_id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def getAdminListByLang(self, search, sort, order, offset, limit, lang):
        """view Admin list # 查询管理员或人员列表

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            id (int): Notice_content object id
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []

        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Admin.query.filter(Admin.id.in_(ids)).filter(Admin.lang.in_((lang, 'all'))).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data

        if search.startswith( 'ids=' ) and len(search)>3 :
            ids = search[4:]
            ids = int(ids)
            pages = db.session.query(Admin). \
                filter(Admin.lang.in_((lang, 'all'))). \
                filter(Admin.status == 1). \
                filter(Admin.id == Notice_contentAdmin.admin_id). \
                filter(Notice_contentAdmin.notice_content_id == ids). \
                paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data
        temp_query_obj = Admin.query
        if lang.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Admin.lang.in_((lang, 'all')))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Admin.title.like("%{search}%".format(search=search)))
        if sort.strip() != '':
            temp_query_obj = temp_query_obj.order_by(eval("Admin."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '': 
            pages = temp_query_obj.order_by(Admin.weight.desc()).order_by(Admin.created.desc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getListByLangAndUid(self, search, sort, order, offset, limit, lang, uid):
            """view list # 查询内容列表

            condition: pagination by lang

            Args:
                search (str): search field, default is title field
                sort (str): sort field
                order (str): order type (asc/desc), default is asc
                offset (int): Paging offset
                limit (int): Maximum number of records per page
                lang (str): language
                uid (int): user id
                
            Returns:
                object: data, for example: {"rows": lst, "total":pages.total}

            """
            data = {}
            page = offset // limit + 1
            temp_query_obj = None
            pages = None
            lst = []
            if search == 'status=1' :
                temp_query_obj = db.session.query(Notice_content.id,Notice_content.title,Notice_content.icon,Notice_contentAdmin.status)
            else :
                temp_query_obj = db.session.query(Notice_content.id,Notice_content.weight,Notice_content.created, Notice_content.updated, Notice_content.title,Notice_content.content,Notice_content.icon,Notice_content.reference,Notice_content.reference_params,Notice_contentAdmin.status,Notice_contentAdmin.created.label('receive_created'), Notice_contentAdmin.id.label('receive_id'))
            if lang.strip() != '' :
                temp_query_obj = temp_query_obj.filter(Notice_content.lang.in_((lang, 'all')))
            if search.strip() != '' :
                if search == 'status=1' :
                    temp_query_obj = temp_query_obj.filter(Notice_contentAdmin.status == 1)
                elif search == 'status=0' :
                    temp_query_obj = temp_query_obj.filter(Notice_contentAdmin.status == 0)
                else :
                    temp_query_obj = temp_query_obj.filter(Notice_content.title.like("%{search}%".format(search=search)))
            if sort.strip() != '' :
                temp_query_obj = temp_query_obj.order_by(eval("Notice_content."+sort+"."+order+"()"))
            if search.strip() == '' and sort.strip() == '' :
                pages = temp_query_obj.filter(Notice_content.id == Notice_contentAdmin.notice_content_id).filter(Notice_contentAdmin.admin_id == uid).order_by(Notice_contentAdmin.status.desc()).order_by(Notice_content.weight.desc()).order_by(Notice_content.created.desc()).paginate(page, limit)
            else :
                pages = temp_query_obj.filter(Notice_content.id == Notice_contentAdmin.notice_content_id).filter(Notice_contentAdmin.admin_id == uid).paginate(page, limit)
            if pages:
                for item in pages.items:
                    lst.append(item)
                data =  {"rows": lst, "total":pages.total}
            return data

    def read_edit(self, id, status):
        """Read Status Modify # 已读状态修改

        Args:
            id (int): notice content id # 内容ID
            status (int): status, 1: Already read 0 : unread # 已读状态， 1：已读， 0： 未读

        Returns:
            bool: True or False

        """
        notice_contentAdminDao = Notice_contentAdminDao()     
        result = notice_contentAdminDao.read_edit(id, status)          
        return result
    