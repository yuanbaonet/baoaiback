"""resource

API Resource Of Profiles Module 

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from flask import current_app,request
from flask_restplus._http import HTTPStatus
from app.common.schema import *
from app.common.param import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from .model import *
from .schema import *
from .param import *
import random
import string
from sqlalchemy import or_
from .dao import *
from app.common.wrap import auth

ns = Namespace("profiles", description="profiles API Resource")

@ns.route("/")
class ProfilesAPI(Resource):
    @ns.parameters(ProfilesParameters(dump_only=['id']))
    @ns.response(ProfilesSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add
        """
        profiles = None
        profilesDao = ProfilesDao()
        try:
            profiles = profilesDao.add(args)
        except Exception as e:
            abort(500, e)       
        return profiles

    @ns.parameters(ProfilesParameters())
    @ns.response(ProfilesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit
        """
        record = None
        profilesDao = ProfilesDao()            
        try:
            record = profilesDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @auth()
    @ns.response(ProfilesSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        view
        """
        record = None
        profilesDao = ProfilesDao() 
        uid = request.uid
        record = profilesDao.getByUid(uid)  
        if not record :
            abort(500, 'Profiles Info is Null')   
        return record



