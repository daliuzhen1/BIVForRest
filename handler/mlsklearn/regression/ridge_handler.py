import tornado
import json  
import uuid
import pandas as pd
from sklearn.linear_model import Ridge
from handler.mlsklearn.util import *
from data.ml_object import MlObject
from data.data_storage import DataStorage
class RidgeHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.body:
                json_data = json.loads(self.request.body)
                Ridge_argstr = ['alpha','fit_intercept', 'normalize', 'copy_X', 'max_iter', 'tol', 'solver', 'random_state']
                sklearn_arg = regqeust_arg_to_sklearn_arg(json_data['sklearn'], Ridge_argstr)
                ridgeHander = Ridge(**sklearn_arg)
            else:
                ridgeHander = Ridge()
            mlobj = MlObject.create_MlObject_by_obj(ridgeHander)
            result = {}
            result['objectID'] = mlobj.object_id
            self.write(json.dumps(result))
        except Exception as e:
            self.write(str(e))


class RidgeParametersHandler(tornado.web.RequestHandler):
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
            result = get_parameter_from_sklearn_object(clf, ['alpha', 'fit_intercept', 'normalize', 'copy_X', 'max_iter', 'tol', 'solver', 'random_state'], sklearn_arg) 
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
                set_parameter_from_sklearn_object(clf, ['alpha', 'fit_intercept', 'normalize', 'copy_X', 'max_iter', 'tol', 'solver', 'random_state'], sklearn_arg) 
                MlObject.save_MlObject_by_obj_id(clf, object_id)
            else:
                raise Exception("please input arguments")
            return
        except Exception as e:
            self.write(str(e))

class RidgeAttributesHandler(tornado.web.RequestHandler):
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
            if 'n_iter_' in sklearn_arg:
                result['n_iter_'] = clf.n_iter_.tolist()
            if not result:
                raise Exception("please input valid sklearn arg")      
            self.write(json.dumps(result))
            return
        except Exception as e:
            self.write(str(e))


class RidgeFitHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            sklearn_fit_for_handler(self, ['sample_weight'])
            return
        except Exception as e:
            self.write(str(e))

class RidgePredictHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            sklearn_predict_for_handler(self)
            return
        except Exception as e:
            self.write(str(e))

class RidgeScoreHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            sklearn_score_for_handler(self, ['sample_weight'])
            return
        except Exception as e:
            self.write(str(e))