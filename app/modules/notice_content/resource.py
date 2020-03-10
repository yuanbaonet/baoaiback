"""

RESTful API Notice Content resource

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-11-30 02:22:26
"""

from app import db
from flask import current_app,request
from app.common.schema import *
from app.common.param import *
from app.common.wrap import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from sqlalchemy import or_
from .model import *
from .schema import *
from .param import *
from .dao import *
from app.modules.admin.schema import *
from app.modules.notice_content_admin.schema import *


ns = Namespace("notice_content", description="RESTful API Notice Content resource")

@ns.route("/")
class Notice_contentAPI(Resource):
    """
    Notice Content module resource main service: add/delete/edit/view
    """
    @ns.parameters(Notice_contentParameters(dump_only=['id']))
    @ns.response(Notice_contentSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        record = None
        notice_contentDao = Notice_contentDao()
        try:
            record = notice_contentDao.add(args)
        except Exception as e:
            abort(500, e)       
        return record

    @ns.parameters(Notice_contentParameters())
    @ns.response(Notice_contentSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        notice_contentDao = Notice_contentDao()            
        try:
            record = notice_contentDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        delete
        """
        result = False
        ids = args.get('ids')
        notice_contentDao = Notice_contentDao()     
        try:
            result = notice_contentDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @auth()
    @ns.parameters(IDParameters())
    @ns.response(Notice_contentSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        notice_contentDao = Notice_contentDao() 
        id = args.get('id')
        record = notice_contentDao.getById(id)  
        return record

@ns.route("/list")
class Notice_contentListAPI(Resource):
    """
    Notice Content module resource list service
    """
    @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(Notice_contentListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')

        notice_contentDao = Notice_contentDao() 
        
        args.setdefault('receiver',0)
        receiver = args.pop('receiver')
        data = notice_contentDao.getListByLangAndReceiver(search, sort, order, offset, limit, lang, receiver)
        
        return data

@ns.route("/list_admin")
class Notice_contentListAdminAPI(Resource):
    """
    Relation Admin List Service
    """
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(AdminListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        Relation Admin List
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')

        notice_contentDao = Notice_contentDao() 
        data = notice_contentDao.getAdminListByLang(search, sort, order, offset, limit, lang)
        return data

@ns.route("/admin")
class Notice_contentAdminAPI(Resource):
    """
    Admin of Notice_contentAdmin service: add/delete
    """
    @ns.parameters(UIDAndIDSParameters())
    @ns.response(Notice_contentAdminSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        record = None
        id = args.get('uid')
        ids = args.get('ids')
        notice_contentDao = Notice_contentDao()
        try:
            record = notice_contentDao.addAdmin(id, ids)
        except Exception as e:
            abort(500, e)       
        return record

    @auth()
    @ns.parameters(UIDAndIDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        delete
        """
        result = False
        id = args.get('uid')
        ids = args.get('ids')
        notice_contentDao = Notice_contentDao()
        try:
            result = notice_contentDao.deleteAdmin(id, ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

@ns.route("/listbyuid")
class Notice_contentListByUidAPI(Resource):
    """
    Notice Content module resource list service
    """
    @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(Notice_contentListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('lang','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        notice_contentDao = Notice_contentDao() 
        args.setdefault('receiver',0)
        receiver = args.pop('receiver')
        uid = request.uid
        data = notice_contentDao.getListByLangAndUid(search, sort, order, offset, limit, lang, uid)
        
        return data

@ns.route("/read_edit")
class Notice_contentReadEditAPI(Resource):
    @ns.parameters(ReadStatusParameters())
    @ns.response(BasicSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """Read Status Modify # 已读状态修改

        Args:
            id (int): notice content id # 内容ID
            status (int): status, 1: Already read 0 : unread # 已读状态， 1：已读， 0： 未读

        Returns:
            bool: True or False
        """
        args.setdefault('id',0)
        id = args.pop('id')
        args.setdefault('status',0)
        status = args.pop('status')
        result = False
        notice_contentAdminDao = Notice_contentAdminDao()     
        try:
            result = notice_contentAdminDao.read_edit(id, status)
        except Exception as e:
            abort(500, e)
        return {"status":result}
