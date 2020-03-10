"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Profiles
from flask import current_app

class ProfilesDao(object):
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
                Profiles.query.filter(Profiles.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def deleteByUid(self, uids):
        """delete by user id

        Args:
            ids (list): user id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Profiles.query.filter(Profiles.uid.in_(tuple(uids))).delete(synchronize_session=False)
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
            object: Profiles object

        """
        profiles = None
        try:
            profiles = Profiles(**args)
            db.session.add(profiles)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return profiles

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Profiles object

        """
        id = args.pop('id')
        uid = args.pop('uid')
        record = Profiles.query.get(id)
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
            object: Profiles object

        """
        record = Profiles.query.get(id)
        return record

    def getByUid(self, uid):
        """view by id

        Args:
            uid (int): uid
            
        Returns:
            object: Profiles object

        """
        record = Profiles.query.filter(Profiles.uid==uid).first()
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
            temp_query_obj = Profiles.query.filter(Profiles.title.like("%{search}%".format(search=search)))   
        if sort.strip() != "" and temp_query_obj == None:
            temp_query_obj = Profiles.query.order_by(eval("Profiles."+sort+"."+order+"()"))
        if sort.strip() != "" and temp_query_obj != None: 
            temp_query_obj = temp_query_obj.order_by(eval("Profiles."+sort+"."+order+"()"))
        if temp_query_obj == None :
            pages = Profiles.query.order_by(Profiles.pid.asc()).order_by(Profiles.weight.desc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit)
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data


