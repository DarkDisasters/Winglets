# from handler.mongohandler import MONGODBHANDLER
# from handler.kdehandler import KDEHandler
# from handler.wingletstephandler import WingletsStepHandler
# from handler.drawhandler import DrawAllHandler
from .kdehandler import KDEHandler
from .wingletstephandler import WingletsStepHandler
from .drawhandler import DrawAllHandler

# class DataInputHandler():
#     def __init__(self, inputType):
#         self.dataInputType = inputType
#         myDB = MONGODBHANDLER()
#         myDB.connectDB('First', 'localhost', 27017)

class OperationHandler():
    def __init__(self, onlyWinglets=True, onlyCircle=False, onlyCommonFate=False, onlyProximity=False):
        # self.curData = DataInputHandler()
        self.kdeHandler = KDEHandler()
        self.wingletsStepHandler = WingletsStepHandler()
        self.drawHandler = DrawAllHandler()
        self.drawCircleHandler, self.drawKDEHandler, self.drawMainContourHandler, self.drawContourHandler, self.drawWingletsHandler = self.drawHandler.init(onlyWinglets, onlyCircle, onlyCommonFate, onlyProximity)
    
    def mapColor(self, colorArr, data):
        self.drawHandler.initGlobalColor(colorArr, data)

    def drawCircle(self, data):
        modifiedDots, clusterInfo, globalMaxDensityPoints, proximityPoints = self.kdeHandler.computeKDE(data)
        self.drawHandler.getInfo(clusterInfo['clusters'], globalMaxDensityPoints, proximityPoints)
        self.drawCircleHandler.drawCircleTest(clusterInfo['clusters'], globalMaxDensityPoints)

    def drawWinglets(self, data):
        # dots = myDB.getDots(fieldsName)['dots']
        modifiedDots, clusterInfo, globalMaxDensityPoints, proximityPoints = self.kdeHandler.computeKDE(data)
        self.drawHandler.getInfo(clusterInfo['clusters'], globalMaxDensityPoints, proximityPoints)
        self.drawCircleHandler.drawCircleTest(clusterInfo['clusters'], globalMaxDensityPoints)
        # drawCircleHandler.drawProximityCircle(proximityPoints)
        # drawCircleHandler.drawCommonFateCircle(clusterInfo['clusters'])
        # drawKDEHandler.drawKDEMap(clusterInfo['clusters'])
        self.drawContourHandler.drawContour(clusterInfo['clusters'])
        self.drawMainContourHandler.drawMainContour(clusterInfo['clusters'])
        # print('*******')
        # curClusterInfo, mapClassIdDotIndexStroke, liMainContour = self.wingletsStepHandler.startDrawWinglets(data, clusterInfo)
        # self.drawMainContourHandler.drawTwoPointLine(curClusterInfo, mapClassIdDotIndexStroke)
        # self.drawWingletsHandler.generateWings(curClusterInfo, mapClassIdDotIndexStroke)

    def drawCommonFateEffect(self, data):
        modifiedDots, clusterInfo, globalMaxDensityPoints, proximityPoints = self.kdeHandler.computeKDE(data)
        self.drawHandler.getInfo(clusterInfo['clusters'], globalMaxDensityPoints, proximityPoints)
        self.drawCircleHandler.drawCircleTest(clusterInfo['clusters'], globalMaxDensityPoints)

    def drawProximityEffect(self, data):
        modifiedDots, clusterInfo, globalMaxDensityPoints, proximityPoints = self.kdeHandler.computeKDE(data)
        self.drawHandler.getInfo(clusterInfo['clusters'], globalMaxDensityPoints, proximityPoints)
        self.drawCircleHandler.drawCircleTest(clusterInfo['clusters'], globalMaxDensityPoints)

    def endDraw(self):
        self.drawHandler.endDraw()
    # def drawWinglets(self):


 

