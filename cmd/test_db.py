import pymongo

myclient = pymongo.MongoClient("mongodb://root:root@localhost:27017")

print(myclient.list_database_names())