import pymongo
from pymongo import MongoClient

# dbIp = 'localhost'


class MONGODBHANDLER:
    def connectDB(self, dbName, dbIp, port):
        self._connection = MongoClient(dbIp, port)
        # print(self._connection.list_database_names())
        self._db = self._connection[dbName]
        collectionName = 'points'
        self._collection = self._db[collectionName]

    def getDots (self, fieldsName):
        return self._collection.find_one({'name': '4'})