"""logging_config

Log Config File

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
import logging.config
# File size in bytes # 文件大小，单位是字节
LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
# The number of rotations # 轮转数量
LOG_FILE_BACKUP_COUNT = 3
log_config = \
{
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "normal_formatter":{
            "format":"%(asctime)s %(levelname)s %(process)d %(thread)d [%(pathname)s:%(lineno)s] %(message)s"
        },
        "sql_formatter": {
            "format": "%(asctime)s %(levelname)s [%(process)d %(thread)d] %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"normal_formatter",
            "stream":"ext://sys.stdout"
        },
        "debug_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"normal_formatter",
            "filename":"log/debug.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "info_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"normal_formatter",
            "filename":"log/info.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "dao_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"normal_formatter",
            "filename":"log/dao.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "sql_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"sql_formatter",
            "filename":"log/sql.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "error_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"ERROR",
            "formatter":"normal_formatter",
            "filename":"log/errors.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "flask_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"normal_formatter",
            "filename":"log/flask.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        },
        "stock_update_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"normal_formatter",
            "filename":"log/stock_update.log",
            "maxBytes":LOG_FILE_MAX_BYTES,
            "backupCount":LOG_FILE_BACKUP_COUNT,
            "encoding":"utf8"
        }
    },
    "loggers":{
        "dao":{
            "level":"DEBUG",
            "handlers":["dao_file_handler"],
            "propagate":"no"
        },
        "sqlalchemy.engine":{
            "level":"DEBUG",
            "handlers":["sql_file_handler"],
            "propagate":"no"
        },
        "flask.app":{
            "level":"DEBUG",
            "handlers":["flask_file_handler"],
            "propagate":"no"
        },
        "stock_update":{
            "level":"DEBUG",
            "handlers":["stock_update_file_handler"],
            "propagate":"no"
        }
    },
    "root":{
        "level":"INFO",
        "handlers":["console","debug_file_handler","error_file_handler"]
    }
}

logging.config.dictConfig(log_config)
# Usage # 使用方法
# daoLogger = logging.getLogger("dao")
# daoLogger.info('dao')
# daoLoggerSub1 = logging.getLogger("dao.sub1")
# daoLoggerSub1.error('daoSub1')