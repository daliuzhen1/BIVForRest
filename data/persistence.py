import pymongo
import pandas
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
datasource = config.get(section='ml_rest', option='datasource')
datastorage = config.get(section='ml_rest', option='datastorage')
objectstorage = config.get(section='ml_rest', option='objectstorage')

def init_dir():

	isExists = os.path.exists(datasource)
	if not isExists:
		os.makedirs(datasource) 
	isExists = os.path.exists(datastorage)
	if not isExists:
		os.makedirs(datastorage) 
	isExists = os.path.exists(objectstorage)
	if not isExists:
		os.makedirs(objectstorage)
	print (datasource)


client = pymongo.MongoClient(host='localhost', port=27017)
database_name = 'ml_rest'
file_meta_db_name = 'file_meta'
data_meta_db_name = 'data_meta'
object_db_name = 'object_info'


