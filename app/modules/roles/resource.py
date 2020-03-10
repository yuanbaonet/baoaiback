"""resource

API Resource Of Roles Module 

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from flask import current_app,request
from app.common.status import Status
from app.common.schema import *
from app.common.param import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from app.common.result import Result
from app.common.wrap import auth
from .model import *
from .schema import *
from .param import *
from .dao import *
from sqlalchemy import or_

ns = Namespace("roles", description="roles API Resource")

@ns.route("/")
class RolesAPI(Resource):
    @auth()
    @ns.response(RolesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        view
        """
        record = None
        rolesDao = RolesDao()
        id = request.uid
        record = rolesDao.getById(id)  
        return record

    @auth()
    @ns.parameters(RolesParameters(dump_only=['id']))
    @ns.response(RolesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        roles = None
        rolesDao = RolesDao()
        try:
            roles = rolesDao.add(args)
        except Exception as e:
            abort(500, e)       
        return roles
    
    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema(many=False))
    def delete(self, args):
        """
        del
        """
        result = False
        ids = args.get('ids')
        rolesDao = RolesDao()            
        try:
            result = rolesDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @auth()
    @ns.parameters(RolesParameters())
    @ns.response(RolesSchema(many=False))
    @ns.response(code=HTTPStatus.CONFLICT)
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        rolesDao = RolesDao()            
        try:
            record = rolesDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/list")
class RolesListAPI(Resource):
    """
    roles module resource list service
    """
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(RolesListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        rolesDao = RolesDao()
        data = rolesDao.getList(search, sort, order, offset, limit)
        return data

@ns.route("/menu")
class RolesMenuAPI(Resource):
    @auth()
    @ns.response(RolesSchema(only=['id', 'pid', 'title'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """view roles list (status=1) # 获取角色菜单列表
        """
        rolesDao = RolesDao()
        menu = rolesDao.getMenu()
        return menu