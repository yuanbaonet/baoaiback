"""

IRIS Module Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
"""

from app import db
from .model import *
from flask import current_app
from sqlalchemy import or_, func, distinct
from collections import OrderedDict
from app.common.ml import MachineLearn

class IrisDao(object):
    
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
                Iris.query.filter(Iris.id.in_(tuple(ids))).delete(synchronize_session=False)
                
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
            object: Iris object

        """
        record = None
        try:
            record = Iris(**args)
            db.session.add(record)
            
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return record

    def edit(self, args):
        """edit

        Args:
            args (OrderedDict): form args

        Returns:
            object: Iris object

        """
        id = args.pop('id')
        record = Iris.query.get(id)
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
            object: Iris object

        """
        record = Iris.query.get(id)
        return record

    def getList(self, search, sort, order, offset, limit):
        """view list

        condition: pagination

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        total = 0
        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Iris.query.filter(Iris.id.in_(ids)).offset(offset).limit(limit).all()
            total = db.session.query(func.count(Test.id)).filter(Test.id.in_(ids)).scalar() 
            if pages:
                for item in pages:
                    lst.append(item)
                data =  {"rows": lst, "total": total}
            return data
        temp_query_obj = Iris.query
        total_query_obj = db.session.query(func.count(Iris.id))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Iris.irisclass.like("%{search}%".format(search=search)))
            total_query_obj = total_query_obj.filter(Iris.irisclass.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Iris."+sort+"."+order+"()"))
        pages = temp_query_obj.offset(offset).limit(limit).all()
        total = total_query_obj.scalar() 
        if pages:
            for item in pages:
                lst.append(item)
            data =  {"rows": lst, "total": total}
        return data

    def getListByLang(self, search, sort, order, offset, limit, lang):
        """view list

        condition: pagination by lang

        Args:
            search (str): search field, default is title field
            sort (str): sort field
            order (str): order type (asc/desc), default is asc
            offset (int): Paging offset
            limit (int): Maximum number of records per page
            lang (str): language
            
        Returns:
            object: data, for example: {"rows": lst, "total":pages.total}

        """
        data = {}
        page = offset // limit + 1
        temp_query_obj = None
        pages = None
        lst = []
        total = 0
        if search.startswith( 'id=' ) and len(search)>3 :
            ids = search[3:]
            ids = eval('['+ids+']')
            pages = Iris.query.filter(Iris.id.in_(ids)).offset(offset).limit(limit).all()
            total = db.session.query(func.count(Iris.id)).filter(Iris.id.in_(ids)).scalar() 
            if pages:
                for item in pages:
                    lst.append(item)
                data =  {"rows": lst, "total":total}
            return data
        temp_query_obj = Iris.query
        total_query_obj = db.session.query(func.count(Iris.id))
        if search.strip() != '' :
            temp_query_obj = temp_query_obj.filter(Iris.irisclass.like("%{search}%".format(search=search)))
            total_query_obj = total_query_obj.filter(Iris.irisclass.like("%{search}%".format(search=search)))
        if sort.strip() != '' :
            temp_query_obj = temp_query_obj.order_by(eval("Iris."+sort+"."+order+"()"))
        pages = temp_query_obj.offset(offset).limit(limit).all()
        total = total_query_obj.scalar() 
        if pages:
            for item in pages:
                lst.append(item)
            data =  {"rows": lst, "total": total}
        return data    

    def linearPredict(self, feature_select, feature_value, linear_select, feature_select_predict):
        """IRIS Linear Predict # 线性预测

        Args:
            feature_select (str): Feature selection of iris, including sepals and petals length and width # 鸢尾花特征选择，包括萼片和花瓣长度、宽度
            feature_value (float): Corresponding value of iris # 鸢尾花对应特征值
            linear_select (str): Linear regression algorithm selection # 线性回归算法选择
            feature_select_predict (str): Prediction feature selection of iris # 鸢尾花预测特征选择           
            
        Returns:
            dict: Iris predict result # 回归预测结果，如 {'linear_result':1.0, 'classify_result':, 'metric':0.9}
        """
        result = {}
        ml = MachineLearn('iris', ["sepal_length","sepal_width","petal_length","petal_width"], ["irisclass"], 0.2)
        data = eval('ml.{linear_select}([feature_select], [feature_select_predict], [[feature_value]])'.format(linear_select=linear_select))
        result['linear_result'] = data[0][0]
        result['classify_result'] = ''
        result['metric'] = data[1]
        return result

    def classifyPredict(self, sepal_length_logic, sepal_width_logic, petal_length_logic, petal_width_logic, logic_select):
        """IRIS Classify Predict # 分类预测

        Args:
            sepal_length_logic (float): sepal length  # 萼片长度
            sepal_width_logic (float): sepal width # 萼片宽度
            petal_length_logic (float): petal length # 花瓣长度
            petal_width_logic (float): petal width # 花瓣宽度 
            logic_select (str): Classification algorithm of iris # 分类算法                
            
        Returns:
            dict: Iris predict result # 分类预测结果，如 {'linear_result':'', 'classify_result':'', 'metric':0.9}
        """
        result = {}
        ml = MachineLearn('iris', ["sepal_length","sepal_width","petal_length","petal_width"], ["irisclass"], 0.2)
        data = eval('ml.{logic_select}([[sepal_length_logic, sepal_width_logic, petal_length_logic, petal_width_logic]])'.format(logic_select=logic_select))
        result['linear_result'] = ''
        result['classify_result'] = data[0][0]
        result['metric'] = data[1]
        return result

    def show(self):
        """Generate Figure # 生成绘图图片，并返回图片路径

        Args:
            
            
        Returns:
            str: figure save path filename
        """
        result = {}
        ml = MachineLearn('iris', ["sepal_length","sepal_width","petal_length","petal_width"], ["irisclass"], 0.2)
        data = ml.showIrisFigure()
        result['figure_name'] = data
        return result


    