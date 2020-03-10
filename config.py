"""config

Config File

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
import os
import uuid

class BasicConfig:
    # 客户访问本API使用地址，请求头中Referer中的值，用于区分是否反向代理
    CLIENT_URL = "http://www.baoai.co/api/"
    SUPER_ROLE = 1 # The role has all rights, value is role's id # 超级角色，拥有所有权限，值为角色的ID
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 # Max upload length # 附件上传最大长度，单位字节
    # JWT Initialization parameters # JWT 认证初始化参数
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a9b374ac-4e30-11ea-8e7f-b42e9995d7c8' # JWT 密钥
    AUTH_SALT = 'd863f34a' # JWT Salt # 盐值
    TOKEN_EXPIRES = 60 * 60 * 24 * 1000 # Token expiration time (Unit: seconds) # 令牌过期时间 (单位：秒)
    REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 1001 # Refresh token expiration time # 更新令牌过期时间

    APP_BLUE_PRINT_URL_PREFIX = "/api" # Define the prefix of blueprint URL # 定义蓝图URL前缀，Flask可以通过蓝图来组织URL以及处理请求
    APP_API_VERSION = "" # BaoAI Open Api Service Version # BaoAI 开放API服务版本
    APP_STATIC_URL_PATH = "/static" # Flask Web Service Static URL Path # Flask Web服务静态URL路径
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__)) # Project Root Absolute Path # 项目根绝对路径
    STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static') # Static File Path # 静态文件路径
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads") # upload file save path # 上传文件保存路径
    MIGRATIONS_FOLDER = os.path.join(PROJECT_ROOT, 'migrations', 'versions') # model migrations file save path # 模型迁移文件保存路径

    # Front-end base paths for automatic code modules # 自动代码模块产生的前端代码保存路径
    FRONT_BASE_FOLDER = "/baoai/baoaifront"

    # Category Root ID # 常用分类ID
    BOOK_CATEGORY_ROOT_ID = 6
    NEWS_CATEGORY_ROOT_ID = 1
    NAV_CATEGORY_ROOT_ID = 13

    # website template folder # Jinja模板默认位置
    SITE_TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'www', 'templates')

    # Cross domain access # 跨域访问
    CORS_ENABLED = True

    # Celery
    CELERY_BROKER_URL = 'redis://:@localhost:6379/2' # 消息代理，用于发布者传递消息给消费者
    CELERY_RESULT_BACKEND = 'redis://:@localhost:6379/2' # 后端，用于存储任务执行结果
    CELERY_REDIS_SCHEDULER_URL = 'redis://:@localhost:6379/2' # 定时任务保存
    CELERY_ENABLE_UTC=True # 启动时区设置
    CELERY_TIMEZONE = 'Asia/Shanghai'  # 设置时区
    CELERYD_CONCURRENCY = 2  # 并发worker数    
    CELERYD_FORCE_EXECV = True    # 非常重要,有些情况下可以防止死锁
    CELERYD_PREFETCH_MULTIPLIER = 4 # 每次去redis取任务的数量，默认值就是4
    CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行100个任务就会被销毁，可防止内存泄露
    # CELERYD_TASK_TIME_LIMIT = 600    # (seconds) Time limits do not currently work on Windows and other platforms that do not support the SIGUSR1 signal. # 秒，单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死 
    # BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90} # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
    # CELERY_DISABLE_RATE_LIMITS = True
    # CELERY_RESULT_SERIALIZER = "json"  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
    # CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显
    # CELERY_TRACK_STARTED = True

    # EMail
    MAIL_SUBJECT = 'Baoai.co Retrieve the password'
    MAIL_SENDER = 'admin@baoai.co'
    MAIL_FROM = 'BaoAI Admin <admin@baoai.co>'
    MAIL_SENDER_PASS = 'xxxxxxxx'
    MAIL_MESSAGE = 'New Password：'
    MAIL_MESSAGE_FAIL = "Respected users, because the system failed to update the password, the current password is reset to the old password, if you still need to update the password to find back, please contact the administrator."

    # Tushare
    TUSHARE_TOKEN = 'wewe323werwsdfw3e243sfszxvcxcvxcvvcxxcv99fdc'
    
    # New user, default rid = 2 role general administrator, (1: super administrator) 
    # 新增用户角色，默认rid = 2 普通，(1: 超级管理员)
    DEFAULT_ADMIN = 2    

    # Operating logging mode, True is recorded in the database, False is recorded in the log file
    # 操作日志记录方式, True 记录到数据库中， False 记录到日志文件中
    LOG_DB = False
    # API response result be recorded? 
    # 是否记录API响应结果
    LOG_RESPONSE = False
    # Table Prefix # 表前缀
    TABLE_PREFIX = "ai_"

    # Flask-SQLAlchemy setting 
    # Flask-SQLAlchemy配置
    SQLALCHEMY_ECHO = True #查询时会显示原始SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = True # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    # SQLALCHEMY_POOL_SIZE = 5 # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_SLOW_DB_QUERY_TIME = 0.01 # 单位秒，查询花费时间较慢的阀值，高于该值将记录flask日志
    # 用于连接数据的数据库
    '''
    SQLite:
    'sqlite:////' + os.path.join(PROJECT_ROOT, 'data-dev.sqlite')
    MySQL-Python:
    mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
    pymysql:
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    MySQL-Connector:
    mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
    cx_Oracle:
    oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
    '''
    # SQLALCHEMY_DATABASE_URI =  os.environ.get('DEV_DATABASE_URL') or \
    #                           'mysql+pymysql://root:root@127.0.0.1:3306/baoai'

    SQLALCHEMY_DATABASE_URI =  os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(PROJECT_ROOT, 'db', 'baoai.db')

    # AI Sample # AI例子
    IRIS_FIGURE = os.path.join(STATIC_FOLDER, "ai", "iris") # iris figure path # 图片存放路径

    def getUUID(self):
        return uuid.uuid1() 

    def getSalt(self):
        return str(uuid.uuid1())[0:8]

class DevelopmentConfig(BasicConfig):
    DEBUG = True
    AUTH = True # Whether authorization is required for API services, using False for testing, and opening authorization for production # 对API服务是否需要授权，测试时使用False, 生产时需要打开授权
    SWAGGERUI = True # Swagger interface document switch, using True in test, False in production # swagger 接口文档开关，测试时使用True, 生产时False
    SWAGGERUI_AUTH = False # Swagger interface document auth switch, test using False # swagger 接口文档权限开关，测试时使用False
    # 用于调试时（1. 无需认证 AUTH=False ，2. swagger 接口调用时无需认证 SWAGGERUI_AUTH=False，3. rbac关闭 ，缺省调试用户）
    DEBUG_USER = 1 # uid=0 用户不存， uid=2, Guest用户 ， uid=1 系统管理员


class TestingConfig(BasicConfig):
    TESTING = True

class ProductionConfig(BasicConfig):
    DEBUG = False
    AUTH = True # Whether authorization is required for API services, using False for testing, and opening authorization for production # 对API服务是否需要授权，测试时使用False, 生产时需要打开授权
    SWAGGERUI = True # Swagger interface document switch, using True in test, False in production # swagger 接口文档开关，测试时使用True, 生产时False
    SWAGGERUI_AUTH = True # Swagger interface document auth switch, test using False # swagger 接口文档权限开关，测试时使用False
    # 用于调试时（1. 无需认证 AUTH=False ，2. swagger 接口调用时无需认证 SWAGGERUI_AUTH=False，3. rbac关闭 ，缺省调试用户）
    DEBUG_USER = 1 # uid=0 用户不存， uid=2, Guest用户 ， uid=1 系统管理员

    SQLALCHEMY_ECHO = False #查询时会显示原始SQL语句
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    # SQLALCHEMY_POOL_SIZE = 5 # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_RECORD_QUERIES = False
    FLASK_SLOW_DB_QUERY_TIME = 1 # 单位秒，查询花费时间较慢的阀值，高于该值将记录flask日志

    TOKEN_EXPIRES = 60 * 60 * 24 * 1 # Token expiration time (Unit: seconds) # 令牌过期时间 (单位：秒)
    REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 2 # Refresh token expiration time # 更新令牌过期时间


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodection': ProductionConfig,
    'default': DevelopmentConfig
}


