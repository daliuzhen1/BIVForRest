import tornado
import pandas as pd
import uuid
import json
import pymongo
from data.persistence import *
from data.data_source import DataSource
from data.data_storage import DataStorage

class DataObjHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data_collection = client[database_name][data_meta_db_name]
            data = json.loads(self.request.body)
            source_id = data.get('sourceID', None)
            data_id = data.get('dataID', None)

            if source_id == None:
                raise Exception("please input source_id")
            DataSource.get_data_source_by_source_id(source_id)
            file_path = datasource + source_id
            column_names = data.get('columnNames', None)
            data_obj = DataStorage.create_data_obj_by_file_path(file_path, column_names)
            if data_obj:
                result = {}
                result['dataID'] = data_obj.data_id
                result['columnNames'] = data_obj.column_names           
                self.write(json.dumps(result))
            else:
                raise Exception("invalid source_id or data_id")
        except Exception as e:
            self.write(str(e))

    def get(self):
        try:
            collection = client[database_name][data_meta_db_name]
            data_id = self.get_argument('dataID', None)
            if data_id == None:
                raise Exception("please input data_id") 
            data_obj = DataStorage.get_data_obj_by_data_id(data_id)
            if data_obj:
                self.set_header('Content-Type', 'application/octet-stream')
                self.set_header('Content-Disposition', 'attachment; filename=%s'%data_id)
                with open(data_obj.file_path, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        self.write(data)
                self.finish()
            else:
                raise Exception("invalid data_id")
        except Exception as e:
            self.write(str(e))