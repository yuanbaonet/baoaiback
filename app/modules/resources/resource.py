"""resource

API Resource Of Resources Module 

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
from app.modules.roles.model import Roles
from app.modules.adminroles.model import AdminRoles

ns = Namespace("resources", description="resources API Resource")

@ns.route("/")
class ResourcesAPI(Resource):
    @auth()
    @ns.response(ResourcesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        view
        """
        record = None
        resourcesDao = ResourcesDao() 
        id = request.uid
        record = resourcesDao.getById(id)  
        return record

    @auth()
    @ns.parameters(ResourcesParameters(dump_only=['id']))
    @ns.response(ResourcesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal Server Exception")
    def post(self, args):
        """
        add
        """
        resources = None
        resourcesDao = ResourcesDao()
        try:
            resources = resourcesDao.add(args)
        except Exception as e:
            abort(500, e)       
        return resources

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def delete(self, args):
        """
        del
        """
        result = False
        ids = args.get('ids')
        resourcesDao = ResourcesDao()
        try:
            result = resourcesDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @auth()
    @ns.parameters(ResourcesParameters())
    @ns.response(ResourcesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        resourcesDao = ResourcesDao()
        try:
            record = resourcesDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/list")
class ResourcesListAPI(Resource):
    """
    resources module resource list service
    """
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(ResourcesListPagerSchema(many=False)) 
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
        resourcesDao = ResourcesDao()
        data = resourcesDao.getList(search, sort, order, offset, limit)
        return data

@ns.route("/menu")
class ResourcesMenuAPI(Resource):
    
    @ns.response(ResourcesSchema(only=['id', 'pid', 'title', 'name'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal Server Exception")
    def get(self):
        """
        get resources menu
        condition: Resources.ismenu==1, Resources.status.in_((1,2))
        """
        record = None
        resourcesDao = ResourcesDao()
        try:
            record = resourcesDao.getMenu()
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/all")
class ResourcesAllAPI(Resource):
    @ns.response(ResourcesSchema(only=['id', 'pid', 'title', 'name'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        get all resources
        condition: Resources.status.in_((1,2))
        """
        record = None
        resourcesDao = ResourcesDao()
        try:
            record = resourcesDao.getAll()
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/routes")
class ResourcesRoutesAPI(Resource):
    @auth()
    @ns.response(ResourcesSchema(many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        get corresponding resources by user id
        """
        record = None
        uid = request.uid
        resourcesDao = ResourcesDao()
        try:
            record = resourcesDao.getRoutes(uid)
        except Exception as e:
            abort(500, e)        
        return record

@ns.route("/weight")
class ResourcesWeightAPI(Resource):
    @auth()
    @ns.response(ResourcesSchema(only=['weight'], many=True))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        get weight max value
        """
        record = None
        resourcesDao = ResourcesDao()
        record = resourcesDao.getWeightMax()
        return record

@ns.route("/reorder")
class ResourcesReorderAPI(Resource):
    @auth()
    @ns.response(BasicSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        del
        """
        result = True
        resourcesDao = ResourcesDao()
        try:
            resourcesDao.setTreeInfoWithAllRecord()
        except Exception as e:
            abort(500, e)
        return {"status":result}