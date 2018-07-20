import tornado
import json  
import uuid
import pandas as pd
from handler.mlsklearn.util import regqeust_arg_to_sklearn_arg
from sklearn.model_selection import train_test_split
from data.persistence import *
from data.data_source import DataSource
from data.data_storage import DataStorage

class TrainTestSplitHandler(tornado.web.RequestHandler):
	def post(self):
		try:
			json_data = json.loads(self.request.body)
			data_id = json_data.get('dataID', None)
			if data_id == None:
				raise Exception("please input data_id")	
			data_column_names = json_data.get('dataColumnNames', None)
			if data_column_names == None:
				raise Exception("please input dataColumnNames")	
			target_column_name = json_data.get('targetColumnName', None)
			if target_column_name == None:
				raise Exception("please input targetColumnName")
			sklearn_arg = json_data.get('sklearn', None)

			data_obj = DataStorage.get_data_obj_by_data_id(data_id)

			if data_obj:
				data_column_names = data_column_names.split(',')
				data = data_obj.pandas_data[data_column_names]
				target = data_obj.pandas_data[target_column_name]
				data = data.values
				target = target.values
				sklearn_arg = regqeust_arg_to_sklearn_arg(sklearn_arg, ['test_size', 'random_state'])
				arrays = [data, target]
				X_train, X_test, y_train, y_test = train_test_split(*arrays, **sklearn_arg)
				X_train = pd.DataFrame(X_train, columns=data_column_names)
				data_obj_X_train = DataStorage.create_data_obj_by_pandas_data(X_train)
				X_test = pd.DataFrame(X_test, columns=data_column_names)
				data_obj_X_test = DataStorage.create_data_obj_by_pandas_data(X_test)
				y_train = pd.DataFrame(y_train, columns=[target_column_name])
				
				data_obj_y_train = DataStorage.create_data_obj_by_pandas_data(y_train)
				y_test = pd.DataFrame(y_test, columns=[target_column_name])
				data_obj_y_test = DataStorage.create_data_obj_by_pandas_data(y_test)
				
				result = {}
				result_X_train = {}
				result_X_train['dataID'] = data_obj_X_train.data_id
				result_X_train['columnNames'] = data_obj_X_train.column_names		
				result_X_test = {}
				result_X_test['dataID'] = data_obj_X_test.data_id
				result_X_test['columnNames'] = data_obj_X_test.column_names		
				result_y_train = {}
				result_y_train['dataID'] = data_obj_y_train.data_id
				result_y_train['columnNames'] = data_obj_y_train.column_names		
				result_y_test = {}
				result_y_test['dataID'] = data_obj_y_test.data_id
				result_y_test['columnNames'] = data_obj_y_test.column_names
				result['X_train'] = result_X_train	
				result['X_test'] = result_X_test	
				result['y_train'] = result_y_train	
				result['y_test'] = result_y_test																			
				self.write(json.dumps(result))
			else:
				raise Exception("invalid source_id")
		except Exception as e:
			self.write(str(e))