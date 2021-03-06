import tornado
import json  
import uuid
import pandas as pd
from sklearn.linear_model import LinearRegression
from handler.mlsklearn.util import *
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
            result = get_parameter_from_sklearn_object(clf, ['fit_intercept', 'normalize', 'copy_X', 'n_jobs'], sklearn_arg) 
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
                set_parameter_from_sklearn_object(clf, ['fit_intercept', 'normalize', 'copy_X', 'n_jobs'], sklearn_arg)
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
            sklearn_fit_for_handler(self, ['sample_weight'])
            return
        except Exception as e:
            self.write(str(e))

class LinearRegressionPredictHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            sklearn_predict_for_handler(self)
            return
        except Exception as e:
            self.write(str(e))

class LinearRegressionScoreHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            sklearn_score_for_handler(self, ['sample_weight'])
            return
        except Exception as e:
            self.write(str(e))