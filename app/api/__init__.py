from flask import Blueprint, current_app
from flask_restplus_patched import Api
from app import Config
from flask_sqlalchemy import get_debug_queries

api_blueprint = Blueprint("open_api", __name__, url_prefix=Config.APP_BLUE_PRINT_URL_PREFIX)
api = Api(api_blueprint, version="1.0",
          prefix=Config.APP_API_VERSION, title="BaoAI", description="BaoAI Open Api Service")

# 查询花费时间较慢的阀值，高于该值将记录flask日志
@api_blueprint.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= Config.FLASK_SLOW_DB_QUERY_TIME :
            current_app.logger.warning('Slow query: %s\nParameters:%s\nDuration:%fs\nContext: %s\n' %(query.statement, query.parameters, query.duration, query.context))
    return response

def init_api(app):
    app.register_blueprint(api_blueprint)