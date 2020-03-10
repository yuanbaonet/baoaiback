from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cluster import KMeans
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import os
from sqlalchemy import create_engine
import matplotlib.pyplot as plt  # python画图包
# import mpld3
from mpld3 import plugins
import seaborn as sns
import uuid
from app import Config

# class Config(object):
#     TABLE_PREFIX = 'ai_'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/baoai'
#     d3_url = 'http://localhost:3000/assets/js/d3.v3.min.js'
#     mpld3_url = 'http://localhost:3000/assets/js/mpld3.v0.3.js'
#     IRIS_FIGURE = '/baoai/BaoAIBack/static/ai/iris'

class MachineLearn(object):
    '''Machine Learn class # 机器学习类

    Automatically read and initialize learning dataset according to module name 
    根据模块名自动读取和初始化学习数据集

    Usage:
    ```
    ml = MachineLearn('iris', ["sepal_length","sepal_width","petal_length","petal_width"], ["irisclass"], 0.2)
    print(ml.LinearRegression(["sepal_length"], ["sepal_width"], [[3]]))
    print(ml.KNNRegressor(["sepal_length"], ["sepal_width"], [[3]]))
    ```
    '''

    def __init__(self, module, x_columns, y_columns, test_size=.2):
        """init 

        init params

        Args:
            module (str): module name
            x_columns (str): x columns
            y_columns (str): y columns
            test_size (float): 测试数据比率
            
        Returns:
            self.con : db connect
            self.module : module name
            self.columns : x_columns + y_columns
            self.x_columns : x_columns
            self.y_columns : y_columns
            self.df : Dataframe
        """
        self.con = None
        self.module = Config.TABLE_PREFIX + module
        self.x_columns = x_columns
        self.y_columns = y_columns
        self.columns = x_columns + y_columns
        self.test_size = test_size
        self.df = None
        try :
            engine =  create_engine(Config.SQLALCHEMY_DATABASE_URI)
            self.con = engine.connect()#创建连接
            # 测试iris, columns=["sepal_length","sepal_width","petal_length","petal_width","irisclass"]
            self.df = pd.read_sql(self.module, self.con, columns=self.columns)
        except Exception as e :
            print(str(e))        
            print('%s Fail'%Config.SQLALCHEMY_DATABASE_URI)  

    def LinearRegression(self, x, y, pred=[[1]]):
        """LinearRegression

        Linear Regression

        Args:
            x (list): x columns name list
            y (list): y columns name list (result)
            pred (list): predict value
            
        Returns:
            object: pred, 

        """
        X = self.df.loc[:,x]
        Y = self.df.loc[:,y]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        #建模
        regr = linear_model.LinearRegression()
        #训练
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        # R2 决定系数（拟合优度）- 模型越好：r2→1 模型越差：r2→0
        metr = metrics.r2_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def KNN(self, pred=[[1,1,1,1]], k=5):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = KNeighborsClassifier(n_neighbors=k)
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def KNNRegressor(self, x, y, pred=[[1]], k=5):
        X = self.df.loc[:,x]
        Y = self.df.loc[:,y]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = KNeighborsRegressor(n_neighbors=k)
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.r2_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def LogisticRegression(self, pred=[[1,1,1,1]], multi_class="multinomial",solver="lbfgs"):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = LogisticRegression(multi_class=multi_class,solver=solver)
        ## bfgs 变尺度法，l-bfgs 限制变尺度法  ，共呃梯度法
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def DecisionTree(self, pred=[[1,1,1,1]], criterion="entropy"):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = DecisionTreeClassifier(criterion=criterion)
        ## criterion -- 默认：gini Gini不纯度   entropy 熵--信息增益IG
        # splitter , best
        # max_depth:树的最大深度， None
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def DecisionTreeReg(self, x, y, pred=[[1]], criterion="mse"):
        X = self.df.loc[:,x]
        Y = self.df.loc[:,y]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = DecisionTreeRegressor(criterion=criterion)
        ## criterion -- 默认：gini Gini不纯度   entropy 熵--信息增益IG
        # splitter , best
        # max_depth:树的最大深度， None
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.r2_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def RandomForest(self,pred=[[1,1,1,1]], n_estimators=10):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = RandomForestClassifier(n_estimators=n_estimators)
        ## n_estimators -- 一般个数越多越好，一般可以取100个
        # max_depth:树的最大深度， None
        # n_job 并行工作个数
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def RandomForestReg(self, x, y, pred=[[1]], n_estimators=10):
        X = self.df.loc[:,x]
        Y = self.df.loc[:,y]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = RandomForestRegressor(n_estimators=n_estimators)
        ## n_estimators -- 一般个数越多越好，一般可以取100个
        # max_depth:树的最大深度， None
        # n_job 并行工作个数
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.r2_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def SVM(self,pred=[[1,1,1,1]], kernel="linear"):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = OneVsRestClassifier(SVC(kernel=kernel)) 
        ## kernel ,linear线性分类
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def SVRReg(self, x, y, pred=[[1]], kernel="linear"):
        X = self.df.loc[:,x]
        Y = self.df.loc[:,y]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)
        regr = SVR(kernel=kernel)
        ## kernel ,linear线性分类
        regr.fit(X_train,Y_train)
        Y_pred = regr.predict(X_test)
        metr = metrics.r2_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,metr

    def KMeans(self,pred=[[1,1,1,1]],n_clusters=3):
        X = self.df.loc[:,self.x_columns]
        Y = self.df.loc[:,self.y_columns]
        X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=self.test_size)

        regr = KMeans(n_clusters=n_clusters)
        regr.fit(X)
        Y_pred = regr.predict(X)
        #metr = metrics.accuracy_score(Y_test,Y_pred)
        pred = regr.predict(pred)
        return pred,0.9

    def showIrisFigure(self):
        fig = plt.figure()        
        sns.pairplot(self.df,hue="irisclass")  
        uuid_code = uuid.uuid1()   
        if  not os.path.exists(Config.IRIS_FIGURE):
            os.makedirs(Config.IRIS_FIGURE)
        fig_save_path = os.path.join(Config.IRIS_FIGURE, str(uuid_code) + ".png")   
        plt.savefig(fig_save_path)
        return str(uuid_code)



    