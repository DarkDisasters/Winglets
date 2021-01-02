import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web

from tornado.options import options, define

import os

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

setting = dict(
    static_path=os.path.join(os.path.dirname(__file__), './'),
    template_path=os.path.join(os.path.dirname(__file__), './'),

)

url = []

application = tornado.web.Application(
    handlers=url,
    debug=True,
    **setting
)

serverPort = 30001
define("port", default=serverPort, help="run on the given port", type=int)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    print('Development server is running at http://127.0.0.1:%s/' % options.port)
    print('Quit the server with Control-C')
    tornado.ioloop.IOLoop.instance().start()

# if __name__ == '__main__':
#     testName = 'dots'
#     outputDots(testName)
#     main()
import Winglets;



myDB = MONGODBHANDLER()
myDB.connectDB('First', 'localhost', 27017)
dots = myDB.getDots('dots')['dots']
Winglets.draw(dots)
main()
