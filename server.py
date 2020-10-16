import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web

from tornado.options import options,define

import os

setting = dict(
   static_path = os.path.join(os.path.dirname(__file__), './'),
   template_path = os.path.join(os.path.dirname(__file__), './'),
   
)

url = []

application = tornado.web.Application(
    handlers=url,
    debug = True,
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

from handler.handler_all import *

if __name__ == '__main__':
    testName = 'dots'
    outputDots(testName)
    main()
    