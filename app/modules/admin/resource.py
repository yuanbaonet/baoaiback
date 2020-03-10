"""resource

API Resource

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from flask import current_app, request, session
from app.common.status import Status
from app.common.schema import *
from app.common.param import *
from flask_restplus_patched import Resource, Namespace, abort, HTTPStatus
from app.common.result import Result
from app.common.wrap import auth
from app.common.captcha import CaptchaTool
from .model import *
from .schema import *
from .param import *
from .dao import *

ns = Namespace("admin", description="admin API Resource")

@ns.route("/")
class AdminAPI(Resource):

    @auth()
    @ns.response(AdminSchema())
    @ns.response(code=HTTPStatus.NO_CONTENT)
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        view # 查看
        """
        record = None
        adminDao = AdminDao() 
        id = request.uid
        record = adminDao.getById(id)  
        return record

    @auth()
    @ns.parameters(AdminParameters(dump_only=['id']))
    @ns.response(AdminSchema(exclude=['password_hash']))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add # 增加
        """
        admin = None
        adminDao = AdminDao()
        try:
            admin = adminDao.add(args)
        except Exception as e:
            abort(500, e)       
        return admin

    @auth()
    @ns.parameters(AdminParameters())
    @ns.response(AdminSchema(exclude=['password_hash']))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def put(self, args):
        """
        edit # 编辑
        """
        record = None
        adminDao = AdminDao()            
        try:
            record = adminDao.edit(args)
        except Exception as e:
            abort(500, e)        
        return record

    @auth()
    @ns.parameters(IDSParameters())
    @ns.response(BasicSchema())
    def delete(self, args):
        """
        del # 删除
        """
        result = False
        ids = args.get('ids')
        adminDao = AdminDao()      
        try:
            result = adminDao.delete(ids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

@ns.route("/find_pass")
class FindPassAPI(Resource):
    @ns.parameters(FindPassParameters())
    @ns.response(BasicSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        Retrieve the password # 找回密码
        """   
        result = False    
        receiver = args.get('email')
        adminDao = AdminDao()      
        try:
            result = adminDao.findPass(receiver)
        except Exception as e:
            abort(500, e)
        if result:
            return Result.success()
        return Result.error()

@ns.route("/login")
class AdminLoginAPI(Resource):
    @ns.parameters(AdminLoginParameters())
    @ns.response(BasicSchema(many=False)) 
    def post(self, args):
        """
        Login # 登录
        """
        data = {}
        username = args.pop('username')
        password = args.pop('password')
        adminDao = AdminDao()      
        try:
            data = adminDao.login(username, password)
        except Exception as e:
            abort(500, e)
        if data:
            return Result.success(data)
        return Result.error(data, message="Account or Password Error")

@ns.route("/rftoken")
class RefleshTokenAPI(Resource):
    @ns.parameters(RefleshTokenParameters())
    @ns.response(BasicSchema(many=False)) 
    def post(self, args):
        """
        Reflesh Token # 刷新令牌
        """
        data = {}
        rftoken = args.pop('rftoken')
        username = args.pop('username')
        adminDao = AdminDao()      
        try:
            data = adminDao.reflesh_token(rftoken, username)
        except Exception as e:
            abort(500, e)
        if data:
            return Result.success(data)
        return Result.error(data, message="Reflesh Token Fail")

@ns.route("/logout")
class AdminLogoutAPI(Resource):
    """
    Logout # 管理员登出
    """
    def get(self):
        """
        Admin logout - Get.
        """
        return self.post()

    @ns.response(BasicSchema(many=False)) 
    def post(self):
        """
        Admin logout - Post.
        """
        data = {}
        return Result.success(data)

@ns.route("/list")
class AdminListAPI(Resource):
    """
    admin list service # 管理员列表
    """
    @auth()
    @ns.parameters(PagerParameters())
    @ns.response(AdminListPagerSchema(many=False)) 
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
        adminDao = AdminDao()  
        data = adminDao.getList(search, sort, order, offset, limit)
        return data

@ns.route("/user_by_token")
class AdminGetAPI(Resource):
    @auth()
    @ns.response(AdminSchema(exclude=['password_hash']))
    @ns.response(code=HTTPStatus.NO_CONTENT)
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        view user by token # 通过令牌获取用户信息
        """
        record = None
        adminDao = AdminDao() 
        uid = request.uid
        record = adminDao.getById(uid)  
        return record

@ns.route("/adminroles")
class AdminRolesAPI(Resource):
    @ns.parameters(UidsRidsParameters())
    @ns.response(BasicSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        Add admin and roles relationships # 增加用户和角色关系
        """
        result = False
        rids = args.get('rids')
        uids = args.get('uids')
        adminDao = AdminDao()      
        try:
            result = adminDao.addAdminRoles(uids, rids)
        except Exception as e:
            abort(500, e)
        return {"status":result}

@ns.route("/rbac")
class RBACAPI(Resource):
    @auth()
    @ns.response(RolesDetailSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        Get Own RBAC with user token # 使用用户令牌得到RBAC信息
        """
        rbacDetail = {}
        uid = request.uid
        adminDao = AdminDao()      
        try:
            rbacDetail = adminDao.getRBAC(uid)
        except Exception as e:
            abort(500, e)
        return rbacDetail

    @auth()
    @ns.parameters(IDJSONParameters())
    @ns.response(RolesDetailSchema(many=False))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        Get RBAC with user id # 用户ID获取RBAC信息
        """
        rbacDetail = {}
        uid = args.get('id')
        adminDao = AdminDao()      
        try:
            rbacDetail = adminDao.getRBAC(uid)
        except Exception as e:
            abort(500, e)
        return rbacDetail

@ns.route("/captcha")
class AdminCaptchaAPI(Resource):
    # @auth()
    @ns.response(BasicSchema())
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def get(self):
        """
        add # 增加
        """
        new_captcha = CaptchaTool()
        img, code = new_captcha.get_verify_code()
        session["code"] = code 
        current_app.logger.debug('code::')   
        current_app.logger.debug(str(session.get("code", '')))    
        return Result.success(img)

@ns.route("/reg")
class AdminRegAPI(Resource):
    # @auth()
    @ns.parameters(AdminParameters(dump_only=['id']))
    @ns.response(AdminSchema(exclude=['password_hash']))
    @ns.response(code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def post(self, args):
        """
        add # 增加
        """
        args.setdefault('avatar','')
        code = args.pop('avatar')
        s_code = session.get("code", '')
        current_app.logger.debug('reg s_code::')   
        current_app.logger.debug(str(s_code))
        if not code or code != s_code :
            abort(500, 'CAPTCHA Failed') 
        admin = None
        adminDao = AdminDao()
        try:
            admin = adminDao.add(args)
        except Exception as e:
            abort(500, e)       
        return admin

