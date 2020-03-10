"""wrap

Verify token and role permissions
验证JWT令牌和角色权限

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from functools import wraps
from flask import request, jsonify, current_app
from flask_restplus import reqparse
from flask_restplus_patched import abort, HTTPStatus
from app.common.status import Status
from app.common.result import Result
from app.modules.admin.model import Admin
from app.modules.adminroles.model import AdminRoles
from app.modules.roles.model import Roles
from app.modules.resources.model import Resources
from app.modules.logs.model import Logs
from app.modules.logs.dao import LogsDao
from app.api import api
from app import db, Config
import collections

def isAuth(uid, route, method):
    """Verify permissions 权限验证

    Judge whether there is access to the resource according to the user ID, access route and access method
    根据用户ID、访问路由和访问方法判断是否有访问该资源权限
    True 充许访问， False 不充许访问

    Args:
        uid (str): user id
        route (str): route , For example: /admin # 访问路由
        method (str): method , For example: GET , POST # 记问方法，如 GET 、 POST
        
    Returns:
        bool: True or False # True 充许访问， False 不充许访问

    """
    resources_ids_list = []
    roles = db.session.query(Roles.id.label('rid') , Roles.title.label('title'), Roles.resources.label('resources')). \
        filter(Roles.status == 1). \
        filter(Roles.id == AdminRoles.rid). \
        filter(AdminRoles.uid == uid). \
        all()   
    if roles :
        for role in roles :
            if role.rid == Config.SUPER_ROLE : # SUPER ROLE has all rights
                return True
            resources_ids_list = resources_ids_list + eval('['+role.resources+']')
    resources = None
    resources = Resources.query.filter(Resources.status.in_((1,2)), Resources.ismenu==0, Resources.id.in_(tuple(set(resources_ids_list)))).all()
    for resource in resources :
        if resource.route == route and resource.method == method.upper() :
            return True
    return False

def auth(rbac=True):
    """Decorator: Verify token and role permissions # 装饰器：验证令牌和角色权限

    Args:
        rbac (bool): True : need auth , False : no auth # True:需要认证， False：无需认证
            
    Usage：
    ```
    @auth()
    def function():
        pass
    
    @auth(False)
    def function():
        pass
    ```
    """
    def wrap_function(func):


        @wraps(func)
        def decorated_view(*args, **kwargs):            
            token = request.headers.get("authtoken")
            # if not token :
            #     abort(500, 'Token is Null')
            method = request.method 
            path = request.path
            base_path = api.base_path
            host_url = request.host_url
            referer = ""
            try :
                referer = request.headers['Referer'] 
            except Exception as e:
                # abort(500, e) 
                pass             
            user_agent = request.headers['User-Agent']
            ip = request.remote_addr
            url = request.url
            route = ""
            desc = "NO AUTH"           
            uid = 0
            if base_path.endswith("/") :
                base_path = base_path[0:-1]
            if path.endswith("/") :
                route = path[len(base_path)+1:-1]
            else :
                route = path[len(base_path)+1:]
            
            # If LOG_DB is True, log to the database # 如果LOG_DB是True, 将日记写入数据库中
            LOG_DB = current_app.config['LOG_DB']
            LOG_RESPONSE = current_app.config['LOG_RESPONSE']
            logs = None
            logsDao = LogsDao()
            if LOG_DB :                               
                logargs = collections.OrderedDict() 
                logargs['uid'] = uid
                logargs['url'] = url  
                logargs['method'] = method         
                logargs['path'] = path
                logargs['base_path'] = base_path
                logargs['referer'] = referer
                logargs['route'] = route
                logargs['ip'] = ip
                logargs['user_agent'] = user_agent
                logargs['desc'] = 'NO AUTH'
                try:
                    logs = logsDao.add(logargs)
                    db.session.commit()
                except Exception as e:
                    # abort(500, e) 
                    pass  
            else :
                current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                    % (uid, url, method, referer , host_url, path, base_path, route, ip, user_agent, desc))   

            # current_app.logger.debug('url: %s , method: %s , referer: %s , path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s' \
            #     % (url, method, referer , path, base_path, route, ip, user_agent))            
            if not current_app.config['AUTH'] :
                request.uid = current_app.config['DEBUG_USER']
                result = func(*args, **kwargs)
                if LOG_RESPONSE :
                    if LOG_DB : 
                        try:
                            logs.desc = str(result)
                            logs = logsDao.add(logargs)
                            db.session.commit()
                        except Exception as e:
                            # abort(500, e) 
                            pass
                    else :
                        current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                            % (uid, url, method, referer , host_url, path, base_path, route, ip, user_agent, str(result)))                      
                return result
            if current_app.config['SWAGGERUI'] and not current_app.config['SWAGGERUI_AUTH'] :
                # referer.startswith(host_url) ， 保存是同一地址发出请求，而不是前端发出
                # not referer.startswith(current_app.config['API_URL'])， 判断是否存在反向代理，如果后台服务地址与CLIENT_URL不同，说明是SWAGGERUI发起
                if referer.startswith(host_url) and not referer.startswith(current_app.config['CLIENT_URL']):
                    request.uid = current_app.config['DEBUG_USER']
                    result = func(*args, **kwargs)
                    if LOG_RESPONSE :
                        if LOG_DB : 
                            try:
                                logs.desc = str(result)
                                logs = logsDao.add(logargs)
                                db.session.commit()
                            except Exception as e:
                                # abort(500, e) 
                                pass
                        else :
                            current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                                % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, str(result)))                      
                    return result
            if not rbac :
                request.uid = current_app.config['DEBUG_USER']
                result = func(*args, **kwargs)
                if LOG_RESPONSE :
                    if LOG_DB : 
                        try:
                            logs.desc = str(result)
                            logs = logsDao.add(logargs)
                            db.session.commit()
                        except Exception as e:
                            # abort(500, e) 
                            pass
                    else :
                        current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                            % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, str(result)))                      
                return result

            data = {}
            if not token:
                desc = 'NO TOKEN'
                if LOG_DB : 
                    try:
                        logs.desc = desc
                        logs = logsDao.add(logargs)
                        db.session.commit()
                    except Exception as e:
                        # abort(500, e) 
                        pass
                else :
                    current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                        % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, desc))  
                abort(code=HTTPStatus.FORBIDDEN, message="TokenError", data=data)

            data = Admin.confirm(token)
            if data.get('status') != Status.TOKEN_SUCCESS.status:
                desc = 'TOKEN AUTH FAILED'
                if LOG_DB : 
                    try:                    
                        logs.desc = desc
                        logs = logsDao.add(logargs)
                        db.session.commit()
                    except Exception as e:
                        # abort(500, e) 
                        pass
                else :
                    current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                        % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, desc)) 
                abort(code=HTTPStatus.FORBIDDEN, message="TokenError", data=data)
            uid = data['data']['id']

            request.uid = uid
            if not isAuth(uid, route, method) :
                desc = 'RBAC AUTH FAILED'                
                if LOG_DB : 
                    try:
                        logs.desc = desc
                        logs.uid = uid
                        logs = logsDao.add(logargs)
                        db.session.commit()
                    except Exception as e:
                        # abort(500, e) 
                        pass
                else :
                    current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                        % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, desc)) 
                abort(code=HTTPStatus.FORBIDDEN, message="NoAccess")
            desc = 'RBAC AUTH SUCCESS'
            if LOG_DB :                 
                try:
                    logs.desc = desc
                    logs.uid = uid
                    logs = logsDao.add(logargs)
                    db.session.commit()
                except Exception as e:
                    # abort(500, e) 
                    pass  
            else :
                current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s  , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                    % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, desc))           
            # return func(*args, **kwargs)
            result = func(*args, **kwargs)
            if LOG_RESPONSE :
                if LOG_DB : 
                    try:
                        logs.desc = str(result)
                        logs.uid = uid
                        logs = logsDao.add(logargs)
                        db.session.commit()
                    except Exception as e:
                        # abort(500, e) 
                        pass
                else :
                    current_app.logger.info('uid: %s , url: %s , method: %s , referer: %s , host_url: %s, path: %s , base_path: %s , route : %s, ip : %s, User-Agent: %s, Desc: %s' \
                        % (uid, url, method, referer, host_url, path, base_path, route, ip, user_agent, str(result)))                      
            return result

        return decorated_view

    return wrap_function

# Singleton Decorator # 单例装饰器
def SingletonDecorator(cls):
    _instance = None
    def get_instance(*args, **kwargs):
        nonlocal _instance
        if _instance is None:
            _instance = cls(*args, **kwargs)
        return _instance
    return get_instance


