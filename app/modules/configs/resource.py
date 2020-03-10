"""resource

API Resource Of Configs Module 

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
from sqlalchemy import or_
from .model import *
from .schema import *
from .param import *
from .dao import *

ns = Namespace("configs", description="configs API Resource")

@ns.route("/")
class ConfigsAPI(Resource):
    """
    configs module resource main service: add/delete/edit/view
    """
    @ns.parameters(ConfigsParameters(dump_only=['id']))
    @ns.response(ConfigsSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        configs = None
        configsDao = ConfigsDao()
        try:
            configs = configsDao.add(args)
        except Exception as e:
            abort(500, e)       
        return configs

    @ns.parameters(ConfigsParameters())
    @ns.response(ConfigsSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        configsDao = ConfigsDao()            
        try:
            record = configsDao.edit(args)
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
        configsDao = ConfigsDao()      
        try:
            result = configsDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @auth()
    @ns.response(ConfigsSchema())
    @ns.response(code=HTTPStatus.NO_CONTENT)
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        configsDao = ConfigsDao() 
        id = request.uid
        record = configsDao.getById(id)  
        return record

@ns.route("/list")
class ConfigsListAPI(Resource):
    """
    configs module resource list service
    """
    @auth()
    @ns.parameters(ExtendPagerParameters())
    @ns.response(ConfigsListPagerSchema(many=False)) 
    @ns.response(code=500)
    def get(self,args):
        """
        view list
        """
        data = {}
        args.setdefault('search','')
        args.setdefault('sort','')
        args.setdefault('module_name','')
        args.setdefault('section','')
        search = args.pop('search')
        sort = args.pop('sort')
        order = args.pop('order')
        offset = args.pop('offset')
        limit = args.pop('limit')
        lang = args.pop('lang')
        module_name = args.pop('module_name')
        section = args.pop('section')
        configsDao = ConfigsDao()
        data = configsDao.getList(search, sort, order, offset, limit, lang, module_name, section)
        return data

@ns.route("/modules")
class ConfigsModulesListAPI(Resource):
    """
    all modules list service # 查询所有模块列表
    """
    #@auth()
    @ns.response(ConfigsSchema(only=['module'], many=True)) 
    @ns.response(code=500)
    def post(self):
        """
        view list
        """
        configsDao = ConfigsDao()
        records = configsDao.getModules()
        return records

@ns.route("/sections")
class ConfigsSectionsListAPI(Resource):
    """
    sections list service by module # 获取某个模块下的所有类别(section)
    """
    #@auth()
    @ns.parameters(ConfigsParameters(only=['module']))
    @ns.response(ConfigsSchema(only=['section'], many=True)) 
    @ns.response(code=500)
    def post(self,args):
        """
        view list
        """
        module = args.get('module')
        configsDao = ConfigsDao()
        records = configsDao.getSections(module)
        return records

@ns.route("/keys")
class ConfigsKeysListAPI(Resource):
    """
    keys list service by module, secton and lang # 由模块、类别和语言获取键值对
    """
    #@auth()
    @ns.parameters(ConfigsParameters(only=['module', 'section', 'lang']))
    @ns.response(ConfigsSchema(only=['keys', 'value', 'title'], many=True)) 
    @ns.response(code=500)
    def post(self,args):
        """
        view list
        """
        module = args.get('module')
        section = args.get('section')
        lang = args.get('lang')
        configsDao = ConfigsDao()
        records = configsDao.getKeys(module, section, lang)
        return records

@ns.route("/value")
class ConfigsValueAPI(Resource):
    """
    get value with module, section , lang and key # 由模块、类别、语言和键获取值
    """
    #@auth()
    @ns.parameters(ConfigsParameters(only=['module', 'section', 'lang', 'keys']))
    @ns.response(ConfigsSchema(many=False)) 
    @ns.response(code=500)
    def post(self,args):
        """
        view list
        """
        module = args.get('module')
        section = args.get('section')
        lang = args.get('lang')
        key = args.get('keys')
        configsDao = ConfigsDao()
        records = configsDao.getValue(module, section, lang, key)
        return records

@ns.route("/models")
class ConfigsModelsListAPI(Resource):
    """
    Get Models List
    """
    @auth()
    @ns.response(ConfigsModelsSchema(many=True)) 
    @ns.response(code=500)
    def get(self):
        """
        view list
        """
        configsDao = ConfigsDao() 
        result = configsDao.getModels()
        return result

