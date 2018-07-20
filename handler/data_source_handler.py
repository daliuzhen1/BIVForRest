import tornado
import urllib.request
import pandas as pd
import os
import json
from data.persistence import *
from data.data_source import DataSource

class DataSourceHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            collection = client[database_name][file_meta_db_name]
            data = json.loads(self.request.body)
            source_type = data.get('sourceType', None)
            if source_type == 'myshare':
                url = data.get('url', None)
                if url == None:
                    raise Exception("please input url") 
                source_info = {}
                source_info['url'] = url
            else:
                raise Exception("do not support the source type")
            data_source = DataSource.create_data_source(source_type,source_info)
            result = {}
            result['sourceID'] = data_source.source_id 
            result['columnNames'] = data_source.column_names
            self.write(json.dumps(result)) 
        except Exception as e:
            self.write(str(e))

    def get(self):
        try:
            collection = client[database_name][file_meta_db_name]
            file_id = self.get_argument('fileID', None)
            if file_id == None:
                raise Exception("please input file_id") 
            data_source = DataSource.get_data_source_by_source_id(file_id)
            if data_source:
                self.set_header('Content-Type', 'application/octet-stream')
                self.set_header('Content-Disposition', 'attachment; filename=%s'%file_id)
                with open(data_source.file_path, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        self.write(data)
                self.finish()
            else:
                raise Exception("invalid file_id")  
        except Exception as e:
            self.write(str(e))

    def delete(self):
        try:
            data = json.loads(self.request.body)
            file_id = data.get('fileID', None)  
            if file_id == None:
                raise Exception("please input file_id") 
            DataSource.delete_data_source_by_file_id(file_id)         
        except Exception as e:
            self.write(str(e))