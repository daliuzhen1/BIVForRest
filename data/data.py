import tornado
import pandas as pd
import uuid
import json
import pymongo
from data.persistence import *

class DataObj:
    data_id = None
    column_names = []
    pandas_data = None #numpy data
    file_path = None
    def persistent(self):
        self.pandas_data.to_csv(self.file_path, index = False)

    @classmethod
    def create_data_obj_by_file_path(cls, file_path, column_names):
        data_obj = DataObj()
        data_obj.data_id = str(uuid.uuid1())
        if column_names != None:
            data_obj.pandas_data = pd.read_csv(file_path, usecols=column_names)
            data_obj.column_names = column_names
        else:
            data_obj.pandas_data = pd.read_csv(file_path)
            data_obj.column_names = data_obj.pandas_data.columns.values.tolist()
        data_obj.file_path = datastorage + data_obj.data_id
        data_obj.persistent()
        collection = client[database_name][data_meta_db_name]
        collection.insert({'data_id' : data_obj.data_id, 'column_names':data_obj.column_names, 'file_path':data_obj.file_path })
        return data_obj

    @classmethod
    def create_data_obj_by_pandas_data(cls, pandas_data):
        data_obj = DataObj()
        data_obj.data_id = str(uuid.uuid1())
        data_obj.pandas_data = pandas_data
        data_obj.column_names = data_obj.pandas_data.columns.values.tolist()
        data_obj.file_path = datastorage + data_obj.data_id
        data_obj.persistent()
        collection = client[database_name][data_meta_db_name]
        collection.insert({'data_id' : data_obj.data_id, 'column_names':data_obj.column_names, 'file_path':data_obj.file_path })
        return data_obj    

    @classmethod
    def get_data_obj_by_data_id(cls, data_id):
        collection = client[database_name][data_meta_db_name]
        data_info = collection.find_one({'data_id': data_id})
        data_obj = DataObj()
        data_obj.data_id = data_info['data_id']
        data_obj.column_names = data_info['column_names']
        data_obj.file_path = data_info['file_path']
        data_obj.pandas_data = pd.read_csv(data_obj.file_path)
        return data_obj   



