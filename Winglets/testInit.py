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

def listTransDict(listData):
    dataDict = {}
    for i in range(len(listData)):
        dataDict[i] = []
        for j in range(len(listData[i])):
            curDataDict = {}
            curDataDict['x'] = listData[i][j][0]
            curDataDict['y'] = listData[i][j][1]
            dataDict[i].append(curDataDict)
    return dataDict

def drawCirlce(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'], onlyCicle=True):
    operationInstance = OperationHandler(False, onlyCicle)
    dataDict = {}
    if isinstance(data, list):
        dataDict = listTransDict(data)
    else:
        dataDict = data
    if len(colorArray) < len(dataDict.keys()):
        raise ColorNotEnoughError('colorArray length is not enough')
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawWinglets(dataDict)
    operationInstance.endDraw()

def drawWinglets(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'], onlyWinglets=True):
    # outputDots(testName)
    operationInstance = OperationHandler(onlyWinglets)
    dataDict = {}
    if isinstance(data, list):
        dataDict = listTransDict(data)
    else:
        dataDict = data
    if len(colorArray) < len(dataDict.keys()):
        raise ColorNotEnoughError('colorArray length is not enough')
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawWinglets(dataDict)
    operationInstance.endDraw()

def drawCommonFate(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']):
    operationInstance = OperationHandler(False, False, True, False)
    dataDict = {}
    if isinstance(data, list):
        dataDict = listTransDict(data)
    else:
        dataDict = data
    if len(colorArray) < len(dataDict.keys()):
        raise ColorNotEnoughError('colorArray length is not enough')
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawCommonFateEffect(dataDict)
    operationInstance.endDraw()

def drawProximity(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']):
    operationInstance = OperationHandler(False, False, False, True)
    dataDict = {}
    if isinstance(data, list):
        dataDict = listTransDict(data)
    else:
        dataDict = data
    if len(colorArray) < len(dataDict.keys()):
        raise ColorNotEnoughError('colorArray length is not enough')
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawProximityEffect(dataDict)
    operationInstance.endDraw()


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
# print('dataArray', dataArray)
drawCirlce(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# drawWinglets(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# drawCommonFate(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# drawProximity(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# draw(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
