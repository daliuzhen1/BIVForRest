import tornado
import json  
import uuid
import pandas as pd
from sklearn.linear_model import LinearRegression
from handler.mlsklearn.util import *
from data.ml_object import MlObject
from data.data_storage import DataStorage
class LinearRegressionHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.body:
                json_data = json.loads(self.request.body)
                LinearRegression_argstr = ['fit_intercept', 'normalize', 'copy_X', 'n_jobs']
                sklearn_arg = regqeust_arg_to_sklearn_arg(json_data['sklearn'], LinearRegression_argstr)
                linearHander = LinearRegression(**sklearn_arg)
            else:
                linearHander = LinearRegression()
            print (linearHander.normalize)
            mlobj = MlObject.create_MlObject_by_obj(linearHander)
            result = {}
            result['objectID'] = mlobj.object_id
            self.write(json.dumps(result))
        except Exception as e:
            self.write(str(e))


class LinearRegressionParametersHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            object_id = self.get_argument('objectID', None)
            if object_id == None:
                raise Exception("please input objectID")
            ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)

            sklearn_arg = self.get_argument('sklearn', None)  
            if not sklearn_arg:
                raise Exception("please input sklearn arg")
            sklearn_arg = sklearn_arg.split(",")
            result = {}
            if 'fit_intercept' in sklearn_arg:
                result['fit_intercept'] = clf.fit_intercept
            if 'normalize' in sklearn_arg:
                result['normalize'] = clf.normalize
            if 'copy_X' in sklearn_arg:
                result['copy_X'] = clf.copy_X
            if 'n_jobs' in sklearn_arg:
                result['n_jobs'] = clf.n_jobs
            if not result:
                raise Exception("please input valid sklearn arg")      
            self.write(json.dumps(result))
            return
        except Exception as e:
            self.write(str(e))

    def put(self):
        try:
            if self.request.body:
                data = json.loads(self.request.body)
                object_id = data.get('objectID', None)  
                if object_id == None:
                    raise Exception("please input handlerID")  
                sklearn_arg = data.get('sklearn', None)  
                if not sklearn_arg:
                    raise Exception("please input sklearn arg")
                ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)
                if 'fit_intercept' in sklearn_arg:
                    clf.fit_intercept = sklearn_arg['fit_intercept']
                if 'normalize' in sklearn_arg:
                    clf.normalize = sklearn_arg['normalize']
                if 'copy_X' in sklearn_arg:
                    clf.copy_X = sklearn_arg['copy_X']
                if 'n_jobs' in sklearn_arg:
                    clf.n_jobs = sklearn_arg['n_jobs']
                MlObject.save_MlObject_by_obj_id(clf, object_id)
            else:
                raise Exception("please input arguments")
            return
        except Exception as e:
            self.write(str(e))

class LinearRegressionAttributesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            object_id = self.get_argument('objectID', None)
            if object_id == None:
                raise Exception("please input objectID")
            ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)

            sklearn_arg = self.get_argument('sklearn', None)  
            print (sklearn_arg)
            if not sklearn_arg:
                raise Exception("please input sklearn arg")
            sklearn_arg = sklearn_arg.split(",")
            result = {}
            if 'coef_' in sklearn_arg:
                result['coef_'] = clf.coef_.tolist()
            if 'intercept_' in sklearn_arg:
                result['intercept_'] = clf.intercept_.tolist()
            print (result)
            if not result:
                raise Exception("please input valid sklearn arg")      
            self.write(json.dumps(result))
            return
        except Exception as e:
            self.write(str(e))


class LinearRegressionFitHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.body:
                data = json.loads(self.request.body)
                object_id = data.get('objectID', None)  
                if object_id == None:
                    raise Exception("please input handlerID")
                X_data_id = data.get('XDataID', None)
                if X_data_id == None:
                    raise Exception("please input XDataID")   
                y_data_id = data.get('yDataID', None)
                if y_data_id == None:
                    raise Exception("please input yDataID")   
                x_data_obj = DataStorage.get_data_obj_by_data_id(X_data_id)     
                y_data_obj = DataStorage.get_data_obj_by_data_id(y_data_id)

                ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)
                sklearn = data.get('sklearn', None)
                print (y_data_obj.pandas_data)
                if sklearn: 
                    LinearRegression_argstr = ['sample_weight']
                    sklearn_arg = regqeust_arg_to_sklearn_arg(sklearn, LinearRegression_argstr)
                    clf.fit(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values, **sklearn_arg)
                else:
                    print (y_data_obj.pandas_data.values)
                    clf.fit(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values)
                MlObject.save_MlObject_by_obj_id(clf, object_id)

            else:
                raise Exception("please input arguments")
            return
        except Exception as e:
            self.write(str(e))

class LinearRegressionPredictHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.body:
                data = json.loads(self.request.body)
                object_id = data.get('objectID', None)  
                if object_id == None:
                    raise Exception("please input handlerID")
                X_data_id = data.get('XDataID', None)
                if X_data_id == None:
                    raise Exception("please input X_data_id")   
                x_data_obj = DataStorage.get_data_obj_by_data_id(X_data_id)
                
                ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)
                predict_y = clf.predict(x_data_obj.pandas_data.values)
                predict_y = pd.DataFrame(predict_y,columns=['predict'])
                MlObject.save_MlObject_by_obj_id(clf, object_id)
                data_obj_predict_y = DataStorage.create_data_obj_by_pandas_data(predict_y)  
                if data_obj_predict_y:
                    result = {}
                    result['dataID'] = data_obj_predict_y.data_id
                    result['columnNames'] = data_obj_predict_y.column_names           
                    self.write(json.dumps(result))
            else:
                raise Exception("please input arguments")
            return
        except Exception as e:
            self.write(str(e))

class LinearRegressionScoreHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.body:
                data = json.loads(self.request.body)
                object_id = data.get('objectID', None)  
                if object_id == None:
                    raise Exception("please input handlerID")
                X_data_id = data.get('XDataID', None)
                if X_data_id == None:
                    raise Exception("please input X_data_id")  
                y_data_id = data.get('yDataID', None)
                if y_data_id == None:
                    raise Exception("please input y_data_id")    
                x_data_obj = DataStorage.get_data_obj_by_data_id(X_data_id)
                y_data_obj = DataStorage.get_data_obj_by_data_id(y_data_id)
                
                ml_obj, clf = MlObject.get_MlObject_by_obj(object_id)
                sklearn = data.get('sklearn', None)
                if sklearn:
                    sample_weight = sklearn['sample_weight']
                    if sample_weight:
                        score = clf.score(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values,sample_weight)
                    else:
                        score = clf.score(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values)
                else:
                    score = clf.score(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values)

                MlObject.save_MlObject_by_obj_id(clf, object_id)
                if score:
                    result = {}
                    result['score'] = score
                    self.write(json.dumps(result))
            else:
                raise Exception("please input arguments")
            return
        except Exception as e:
            self.write(str(e))