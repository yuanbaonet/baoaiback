"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Logs
from flask import current_app

class LogsDao(object):
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
                Logs.query.filter(Logs.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def deleteByUid(self, ids, uid):
        """delete

        Args:
            ids (list): id list
            uid (int): user id
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Logs.query.filter(Logs.id.in_(tuple(ids)), Logs.uid==uid).delete(synchronize_session=False)
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
            object: Configs object

        """
        logs = None
        try:
            logs = Logs(**args)
            db.session.add(logs)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return logs

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Configs object

        """
        id = args.pop('id')
        uid = args.pop('uid')
        record = Logs.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
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
            object: Logs object

        """
        record = Logs.query.get(id)
        return record

    def getByUid(self, uid):
        """view by uid

        Args:
            uid (int): user id
            
        Returns:
            object: Logs object

        """
        record = Logs.query.filter(Logs.uid==uid).first()
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
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        if search.strip() != '' :
            temp_query_obj = Logs.query.filter(Logs.title.like("%{search}%".format(search=search)))
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Logs.query.order_by(eval("Logs."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Logs."+sort+"."+order+"()"))
        if temp_query_obj == None :
            pages = Logs.query.order_by(Logs.created.desc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getListByUid(self, search, sort, order, offset, limit, uid):
        """view list

        condition: pagination

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
        if search.strip() != '' :
            temp_query_obj = Logs.query.filter(Logs.uid==uid).filter(Logs.title.like("%{search}%".format(search=search)))    # 如果找不到会抛出404异常
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Logs.query.filter(Logs.uid==uid).order_by(eval("Logs."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Logs."+sort+"."+order+"()"))
        if temp_query_obj == None :
            pages = Logs.query.filter(Logs.uid==uid).order_by(Logs.created.desc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data


