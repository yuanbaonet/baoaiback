"""resource

API Resource Of Logs Module 

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from flask import current_app,request
from app.common.schema import *
from app.common.param import *
from app.common.wrap import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from .model import *
from .schema import *
from .param import *
from sqlalchemy import or_
from .dao import *

ns = Namespace("logs", description="logs API Resource")

@ns.route("/")
class LogsAPI(Resource):
    @ns.parameters(LogsParameters(dump_only=['id']))
    @ns.response(LogsSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        logs = None
        logsDao = LogsDao()
        try:
            logs = logsDao.add(args)
        except Exception as e:
            abort(500, e)       
        return logs

    @ns.parameters(LogsParameters())
    @ns.response(LogsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        logsDao = LogsDao()            
        try:
            record = logsDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @ns.parameters(IDParameters())
    @ns.response(LogsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        logsDao = LogsDao() 
        id = args.get('id')
        record = logsDao.getById(id)  
        return record

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        del
        """
        result = False
        ids = args.get('ids')
        logsDao = LogsDao()      
        try:
            result = logsDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

@ns.route("/list")
class LogsListAPI(Resource):
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(LogsListPagerSchema(many=False)) 
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self,args):
        """
        list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        logsDao = LogsDao()
        data = logsDao.getList(search, sort, order, offset, limit)
        return data

@ns.route("/user")
class UserLogsAPI(Resource):
    @ns.parameters(LogsParameters(dump_only=['id']))
    @ns.response(LogsSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        logs = None
        logsDao = LogsDao()
        try:
            logs = logsDao.add(args)
        except Exception as e:
            abort(500, e)       
        return logs

    @ns.parameters(LogsParameters())
    @ns.response(LogsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        logsDao = LogsDao()            
        try:
            record = logsDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @ns.parameters(IDParameters())
    @ns.response(LogsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        logsDao = LogsDao() 
        id = args.get('id')
        record = logsDao.getById(id)  
        return record

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        del
        """
        result = False
        ids = args.get('ids')
        uid = request.uid
        logsDao = LogsDao()      
        try:
            result = logsDao.deleteByUid(ids, uid)
        except Exception as e:
            abort(500, e)
        return {"status":result}

@ns.route("/user/list")
class UserLogsListAPI(Resource):
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(LogsListPagerSchema(many=False)) 
    @ns.response(code=500,description="Internal Server Exception")
    def get(self,args):
        """
        list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        logsDao = LogsDao()
        uid = request.uid
        data = logsDao.getListByUid(search, sort, order, offset, limit, uid)
        return data



