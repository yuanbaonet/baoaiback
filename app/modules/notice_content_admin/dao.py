"""
notice_content and admin relation module Data Access Object

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
from sqlalchemy import or_

class Notice_contentAdminDao(object):
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
                Notice_contentAdmin.query.filter(Notice_contentAdmin.id.in_(tuple(ids))).delete(synchronize_session=False)
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
            object: Notice_contentAdmin object

        """
        record = None
        try:
            record = Notice_contentAdmin(**args)
            db.session.add(record)
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
            object: Notice_contentAdmin object

        """
        id = args.pop('id')
        record = Notice_contentAdmin.query.get(id)
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
            object: Notice_content object

        """
        record = Notice_contentAdmin.query.get(id)
        return record

    def read_edit(self, id, status):
        """Read Status Modify # 已读状态修改

        Args:
            id (int): notice content id # 内容ID
            status (int): status, 1: Already read 0 : unread # 已读状态， 1：已读， 0： 未读

        Returns:
            bool: True or False
        """
        result = False
        record = Notice_contentAdmin.query.get(id)
        if record :
            try:
                record.status = status
                db.session.commit()
                result = True
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return result




            
                