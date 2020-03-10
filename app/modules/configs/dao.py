"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""

from app import db
from .model import Configs
from flask import current_app
from sqlalchemy import distinct
import inspect
import traceback

class ConfigsDao(object):
    def delete(self, ids):
        """delete

        Args:
            ids (list): id list
            
        Returns:
            bool: True or False

        """
        result = False
        if ids:
            try:
                Configs.query.filter(Configs.id.in_(tuple(ids))).delete(synchronize_session=False)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)
            result = True
        return result

    def add(self, args):
        """add

        Args:
            args (OrderedDict): form args
            
        Returns:
            object: Configs object

        """
        configs = None
        try:
            configs = Configs(**args)
            db.session.add(configs)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return configs

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Configs object

        """
        id = args.pop('id')
        uid = args.pop('uid')
        record = Configs.query.get(id)
        if record :
            try:
                for k,v in args.items():
                    setattr(record,k,v)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise Exception(e)            
        return record

    def getById(self, id):
        """view by id

        Args:
            id (int): id
            
        Returns:
            object: Configs object

        """
        record = Configs.query.get(id)
        return record

    def getList(self, search, sort, order, offset, limit, lang, module_name, section):
        """view list

        condition: pagination

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            module_name (str): module name
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        temp_query_obj = Configs.query
        if lang.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Configs.lang.in_((lang, 'all')))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Configs.title.like("%{search}%".format(search=search)))
        if module_name :
            temp_query_obj = temp_query_obj.filter(Configs.module==module_name)
        if section :
            temp_query_obj = temp_query_obj.filter(Configs.section==section)
        if sort.strip() != '':
            temp_query_obj = temp_query_obj.order_by(eval("Configs."+sort+"."+order+"()"))
        if search.strip() == '' and sort.strip() == '' :
            pages = temp_query_obj.order_by(Configs.module.asc()).order_by(Configs.section.asc()).order_by(Configs.weight.desc()).order_by(Configs.keys.asc()).order_by(Configs.created.asc()).paginate(page, limit)
        else :
            pages = temp_query_obj.paginate(page, limit) 
        lst = []
        if pages:
            for item in pages.items:
                lst.append(item)
            data =  {"rows": lst, "total":pages.total}
        return data

    def getModules(self):
        """view all modules # 获取所有模块

        Args:
            
            
        Returns:
            list: module List

        """
        records = Configs.query.with_entities(distinct(Configs.module).label('module')).order_by(Configs.created.asc()).all()
        return records

    def getSections(self, module):
        """view the module's sections by module name # 获取某个模块下的所有类别(section)

        Args:
            module (str): module name         
            
        Returns:
            list: section List

        """
        records = Configs.query.with_entities(distinct(Configs.section).label('section')).filter(Configs.module==module).order_by(Configs.created.asc()).all()
        return records

    def getKeys(self, module, section, lang):
        """view keys and value with module, section and lang # 由模块、类别和语言获取键值对

        Args:
            module (str): module name
            section (str): section name
            lang (str): lang
            
        Returns:
            list: keys and value list

        """
        records = None
        if not module :
            raise Exception('module is null')
        temp_query_obj = Configs.query.with_entities(Configs.keys, Configs.value, Configs.title).filter(Configs.module==module)
        if section :
            temp_query_obj = temp_query_obj.filter(Configs.section==section)
        if lang :
            temp_query_obj = temp_query_obj.filter(Configs.lang.in_((lang, 'all'))) 
        records = temp_query_obj.order_by(Configs.weight.asc()).order_by(Configs.created.asc()).all()
        return records

    def getValue(self, module, section, lang, key):
        """get value with module, section , lang and key # 由模块、类别、语言和键获取值

        Args:
            module (str): module name
            section (str): section name
            lang (str): lang
            key (str): key
            
        Returns:
            str: value of key # 键对应的值

        """
        record = None
        if not module :
            raise Exception('module is null')
        temp_query_obj = Configs.query.filter(Configs.module==module)
        if section :
            temp_query_obj = temp_query_obj.filter(Configs.section==section)
        if lang :
            temp_query_obj = temp_query_obj.filter(Configs.lang.in_((lang, 'all'))) 
        if key :
            temp_query_obj = temp_query_obj.filter(Configs.keys==key)
        record = temp_query_obj.first()
        return record

    def getModels(self):
        """Get Models Dict

        Args:
            
            
        Returns:
            dict: all models dict, include model's columns, for example: {"rows": lst, "total":pages.total}

        """
        models = []
        for clazz in db.Model._decl_class_registry.values():
            data = {}
            try:
                # current_app.logger.debug(str(clazz))
                model_class_str = str(clazz)
                model_class_slice = model_class_str[0:-2][8:]
                model_class_list = model_class_slice.rsplit('.',1)
                data['model'] = model_class_list[1]
                data['module'] = model_class_list[0].rsplit('.',1)[0]
                data['module_name'] = data['module'].rsplit('.',1)[1]
                clazz_prop = inspect.getmembers(clazz, lambda x: not callable(x))
                data['columns'] = [c.name for c in clazz_prop[0][1].get('__table__').columns]
                data['tablename'] = str(clazz_prop[0][1].get('__table__'))
                # current_app.logger.debug(str(data))
                models.append(data)
            except Exception as e:
                current_app.logger.debug(traceback.format_exc())                
        # current_app.logger.debug(str(models))
        return models


