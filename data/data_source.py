import urllib.request
import pandas as pd
import uuid
import os
import json
from data.persistence import *

class DataSource():
    source_id = None
    file_path = None
    source_type = None
    column_names = None

    @classmethod
    def create_data_source(cls, source_type, source_info):
        data_source = DataSource()
        collection = client[database_name][file_meta_db_name]
        data_source.source_type = source_type
        if data_source.source_type == 'myshare':
            url = source_info['url']
            url_file = urllib.request.urlopen(url)
            data_source.source_id = str(uuid.uuid1())
            print (datasource)
            data_source.file_path = datasource + data_source.source_id
            with open(data_source.file_path,'wb') as output:
                output.write(url_file.read())
                # only support csv now
            columns = pd.read_csv(data_source.file_path, nrows=1).columns
            data_source.column_names = columns.values.tolist()
            collection.insert({'source_id' : data_source.source_id, 'column_names':data_source.column_names, 'source_type':data_source.source_type, 'file_path':data_source.file_path })
        return data_source

    @classmethod
    def get_data_source_by_source_id(cls, source_id):
        collection = client[database_name][file_meta_db_name]
        data_source_db_info = collection.find_one({'source_id':source_id})
        if data_source_db_info:
            data_source = DataSource()
            data_source.source_id = data_source_db_info['source_id']
            data_source.column_names = data_source_db_info['column_names']
            data_source.source_type = data_source_db_info['source_type']
            data_source.file_path = data_source_db_info['file_path']
            return data_source
        else:
            raise Exception('invalid source_id')

    @classmethod
    def delete_data_source_by_source_id(cls, source_id):
        collection = client[database_name][file_meta_db_name]
        data_source_db_info = collection.find_one({'source_id':source_id})
        if data_source_db_info:
            os.remove(data_source_db_info['file_path'])
            collection.remove({'source_id': source_id})
        else:
            raise Exception('invalid source_id')
       



