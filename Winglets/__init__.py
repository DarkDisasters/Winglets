
from .handler.handler_all import *
# from handler import handler_all as AllHandler
# from .handler.handler_all import OperationHandler
# from handler.handler_all import OperationHandler
# import handler.handler_all as AllHandler
import math;

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

def getMaxKey(curDict):
    maxKeyValue = 0
    for key in curDict.keys():
        if maxKeyValue < int(key):
            maxKeyValue = int(key)
    return maxKeyValue

def drawCirlce(data, colorArray = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo'], onlyCicle=True):
    operationInstance = None
    if not onlyCicle:
        operationInstance = OperationHandler(False)
    else:
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
    # if len(colorArray) < len(dataDict.keys()) or len(colorArray) < getMaxKey(dataDict):
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
    # if len(colorArray) < len(dataDict.keys()) or len(colorArray) < getMaxKey(dataDict):
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
    # if len(colorArray) < len(dataDict.keys()) or len(colorArray) < getMaxKey(dataDict):
    if len(colorArray) < len(dataDict.keys()):
        raise ColorNotEnoughError('colorArray length is not enough')
    operationInstance.mapColor(colorArray, dataDict)
    operationInstance.drawProximityEffect(dataDict)
    operationInstance.endDraw()