
from .handler.handler_all import *
# from handler import handler_all as AllHandler
# from .handler.handler_all import OperationHandler
# from handler.handler_all import OperationHandler
# import handler.handler_all as AllHandler

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
        for i in range(len(data)):
            dataDict[i] = []
            for j in range(len(data[i])):
                curDataDict = {}
                curDataDict['x'] = data[i][j][0]
                curDataDict['y'] = data[i][j][1]
                dataDict[i].append(curDataDict)
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


