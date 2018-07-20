
from sklearn.externals import joblib
from data.persistence import *
import uuid

class MlObject:
    object_id = None
    file_path = None

    @classmethod
    def create_MlObject_by_obj(cls, obj):
        ml_obj = MlObject()
        collection = client[database_name][object_db_name]
        ml_obj.object_id = str(uuid.uuid1())
        obj_path = objectstorage + ml_obj.object_id
        ml_obj.file_path = obj_path
        joblib.dump(obj, ml_obj.file_path) 
        collection.insert({'object_id' : ml_obj.object_id, 'file_path':ml_obj.file_path })
        return ml_obj   

    @classmethod
    def get_MlObject_by_obj(cls, obj_id):
        collection = client[database_name][object_db_name]
        ml_object_db_info = collection.find_one({'object_id':obj_id})
        if ml_object_db_info:
            ml_obj = MlObject()
            ml_obj.object_id = ml_object_db_info['object_id']
            ml_obj.file_path = ml_object_db_info['file_path']
            clf = joblib.load(ml_obj.file_path) 
            return ml_obj,clf
        else:
            raise Exception('invalid source_id')

    @classmethod
    def save_MlObject_by_obj_id(cls, obj, obj_id):
        collection = client[database_name][object_db_name]
        ml_object_db_info = collection.find_one({'object_id':obj_id})
        if ml_object_db_info:
            ml_obj = MlObject()
            joblib.dump(obj, ml_object_db_info['file_path']) 
        else:
            raise Exception('invalid source_id')    