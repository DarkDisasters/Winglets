import os
import json

# import sys
# sys.path.insert(0, './')

import handler.handler_all
# from .handler.handler_all import *
# from handler import handler_all as AllHandler
# from .handler.handler_all import OperationHandler
from handler.handler_all import OperationHandler
# import handler.handler_all as AllHandler

# setting = dict(
#     static_path=os.path.join(os.path.dirname(__file__), './'),
#     template_path=os.path.join(os.path.dirname(__file__), './'),

# )

# url = []

# application = tornado.web.Application(
#     handlers=url,
#     debug=True,
#     **setting
# )

# serverPort = 30001
# define("port", default=serverPort, help="run on the given port", type=int)


# def main():
#     tornado.options.parse_command_line()
#     http_server = tornado.httpserver.HTTPServer(application)
#     print('Development server is running at http://127.0.0.1:%s/' % options.port)
#     print('Quit the server with Control-C')
#     tornado.ioloop.IOLoop.instance().start()

# if __name__ == '__main__':
#     testName = 'dots'
#     outputDots(testName)
#     main()

class ColorNotEnoughError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorInfo = ErrorInfo
    def __str__(self):
        return self.errorInfo

def draw(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']):
    # outputDots(testName)
    operationInstance = OperationHandler()
    dataDict = {}
    if isinstance(data, list):
        for i in range(data):
            dataDict[i] = data[i]
    else:
        dataDict = data
    if len(colorArray) < len(dataDict.keys()):
        # print('lenght dataDict', len(dataDict.keys()))
        # try:
        raise ColorNotEnoughError('colorArray length is not enough')
        # except ColorNotEnoughError as e:
        #     print(e)
        # return 0
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawWinglets(dataDict)
    operationInstance.endDraw()
    # main()


dataDict = {}
f = open('./testFile.json', 'r')
dataDict = json.loads(f.read())
# print('dataDict', dataDict)
# draw(dataDict['dots'], ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'])
dataArray = []
for curKey in dataDict['dots'].keys():
    curArrDictData = dataDict['dots'][curKey]
    curKeyArr = []
    for i in range(len(curArrDictData)):
        curKeyArr.append([curArrDictData[i]['x'], curArrDictData[i]['y']])
    dataArray.append(curKeyArr)
print('dataArray', dataArray)
# draw(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
