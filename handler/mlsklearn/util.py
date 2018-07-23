import json  
from data.data_storage import DataStorage
from data.ml_object import MlObject
def regqeust_arg_to_sklearn_arg(reqeust_sklearn_arg, sklearn_arg_list):
    sklearn_arg = {}
    for regqeust_arg_key in reqeust_sklearn_arg:
        if regqeust_arg_key in sklearn_arg_list:
            argvalue = reqeust_sklearn_arg.get(regqeust_arg_key)
            sklearn_arg[regqeust_arg_key] = argvalue
    print(sklearn_arg)
    return sklearn_arg

def check_arg_valid(reqeust_sklearn_arg, sklearn_arg_list, clf):
    sklearn_arg = {}
    reqeust_sklearn_arg = reqeust_sklearn_arg.split(",")
    for regqeust_arg_key in reqeust_sklearn_arg:
        if regqeust_arg_key not in sklearn_arg_list:
            return False
    return True

def get_parameter_from_sklearn_object(clf, obj_parameters, req_parameters):
    result = {}
    for obj_parameter in obj_parameters:   
        if obj_parameter in req_parameters:
            if hasattr(clf, obj_parameter):
                result[obj_parameter] = getattr(clf, obj_parameter)
            else:
                raise Exception('invalid parameter')

def set_parameter_from_sklearn_object(clf, obj_parameters, req_parameters):
    for obj_parameter in obj_parameters:   
        if obj_parameter in req_parameters:
            if hasattr(clf, obj_parameter):
                setattr(clf, obj_parameter, req_parameters[obj_parameter])
            else:
                raise Exception('invalid parameter')

def sklearn_fit_for_handler(handler, fit_arg_array):
    try:
        if handler.request.body:
            data = json.loads(handler.request.body)
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
                sklearn_arg = regqeust_arg_to_sklearn_arg(sklearn, fit_arg_array)
                clf.fit(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values, **sklearn_arg)
            else:
                clf.fit(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values)
            MlObject.save_MlObject_by_obj_id(clf, object_id)
        else:
            raise Exception("please input arguments")
        return
    except Exception as e:
            handler.write(str(e))


def sklearn_predict_for_handler(handler):
    try:
        if handler.request.body:
            data = json.loads(handler.request.body)
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
                handler.write(json.dumps(result))
        else:
            raise Exception("please input arguments")
        return
    except Exception as e:
        handler.write(str(e))

def sklearn_score_for_handler(handler, fit_arg_array):
    try:
        if handler.request.body:
            data = json.loads(handler.request.body)
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
                sklearn_arg = regqeust_arg_to_sklearn_arg(sklearn, fit_arg_array)
                score = clf.score(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values,**sklearn_arg)
            else:
                score = clf.score(x_data_obj.pandas_data.values, y_data_obj.pandas_data.values)

            MlObject.save_MlObject_by_obj_id(clf, object_id)
            if score:
                result = {}
                result['score'] = score
                handler.write(json.dumps(result))
        else:
            raise Exception("please input arguments")
        return
    except Exception as e:
        handler.write(str(e))