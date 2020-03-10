"""

RESTful API IRIS resource

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
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


ns = Namespace("iris", description="RESTful API IRIS resource")

@ns.route("/")
class IrisAPI(Resource):
    """
    IRIS module resource main service: add/delete/edit/view
    """
    @ns.parameters(IrisParameters(dump_only=['id']))
    @ns.response(IrisSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        record = None
        irisDao = IrisDao()
        try:
            record = irisDao.add(args)
        except Exception as e:
            abort(500, e)       
        return record

    @ns.parameters(IrisParameters())
    @ns.response(IrisSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        irisDao = IrisDao()            
        try:
            record = irisDao.edit(args)
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
        irisDao = IrisDao()     
        try:
            result = irisDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

    @auth()
    @ns.parameters(IDParameters())
    @ns.response(IrisSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        view
        """
        record = None
        irisDao = IrisDao() 
        id = args.get('id')
        record = irisDao.getById(id)  
        return record

@ns.route("/list")
class IrisListAPI(Resource):
    """
    IRIS module resource list service
    """
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(IrisListPagerSchema(many=False)) 
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

        irisDao = IrisDao() 
        
        data = irisDao.getListByLang(search, sort, order, offset, limit, lang)
        
        return data

@ns.route("/linear_predict")
class IrisLinearPredictAPI(Resource):
    @auth()
    @ns.parameters(IrisLinearPredictParameters())
    @ns.response(IrisPredictSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """Regression prediction 回归预测

        """
        data = {}
        args.setdefault('feature_select','')
        args.setdefault('feature_value',1)
        args.setdefault('linear_select','')
        args.setdefault('feature_select_predict','')
        feature_select = args.pop('feature_select')
        feature_value = args.pop('feature_value')
        linear_select = args.pop('linear_select')
        feature_select_predict = args.pop('feature_select_predict')
        irisDao = IrisDao()
        data = irisDao.linearPredict(feature_select, feature_value, linear_select, feature_select_predict)
        return data

@ns.route("/classify_predict")
class IrisClassifyPredictAPI(Resource):
    @auth()
    @ns.parameters(IrisClassifyPredictParameters())
    @ns.response(IrisPredictSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self, args):
        """
        classify predict # 分类预测
        """
        data = {}
        args.setdefault('sepal_length_logic',1)
        args.setdefault('sepal_width_logic',1)
        args.setdefault('petal_length_logic',1)
        args.setdefault('petal_width_logic',1)
        args.setdefault('logic_select','')
        sepal_length_logic = args.pop('sepal_length_logic')
        sepal_width_logic = args.pop('sepal_width_logic')
        petal_length_logic = args.pop('petal_length_logic')
        petal_width_logic = args.pop('petal_width_logic')
        logic_select = args.pop('logic_select')
        irisDao = IrisDao()
        data = irisDao.classifyPredict(sepal_length_logic, sepal_width_logic, petal_length_logic, petal_width_logic, logic_select)
        return data

@ns.route("/show")
class IrisLinearPredictAPI(Resource):
    @auth()
    @ns.response(IrisFigureSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        Generate Figure 
        生成绘图图片，并返回图片路径
        """
        data = {}
        irisDao = IrisDao()
        data = irisDao.show()
        return data
