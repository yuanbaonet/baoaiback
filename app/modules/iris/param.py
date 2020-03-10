"""

IRIS Module Request Parameter

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
CREATEDATE: 2019-08-23 16:18:40
"""

from flask_marshmallow import base_fields
from marshmallow import validate
from flask_restplus_patched import Parameters, PostFormParameters, JSONParameters
from .schema import *


class IrisParameters(JSONParameters, IrisSchema):
    """
    IRIS Parameters
    """
    class Meta(IrisSchema.Meta):
        pass

class IrisLinearPredictParameters(Parameters):
    feature_select = base_fields.String(required=False) # Feature selection of iris, including sepals and petals length and width # 鸢尾花特征选择，包括萼片和花瓣长度、宽度
    feature_value = base_fields.Float(required=False) # Corresponding value of iris # 鸢尾花对应特征值
    linear_select = base_fields.String(required=False) # Linear regression algorithm selection # 线性回归算法选择
    feature_select_predict = base_fields.String(required=False) # Prediction feature selection of iris # 鸢尾花预测特征选择

class IrisClassifyPredictParameters(Parameters):
    sepal_length_logic = base_fields.Float(required=False)
    sepal_width_logic = base_fields.Float(required=False)
    petal_length_logic = base_fields.Float(required=False)
    petal_width_logic = base_fields.Float(required=False)
    logic_select = base_fields.String(required=False)


    