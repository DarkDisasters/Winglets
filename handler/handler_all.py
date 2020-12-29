from handler.mongohandler import MONGODBHANDLER
from handler.kdehandler import KDEHandler
from handler.wingletstephandler import WingletsStepHandler
from handler.drawhandler import DrawAllHandler

myDB = MONGODBHANDLER()
myDB.connectDB('First', 'localhost', 27017)

myKdeHandler = KDEHandler()
wingletsStepHandler = WingletsStepHandler()
# cv = Canvas(root, bg='white')


def outputDots(fieldsName):
    drawHandler = DrawAllHandler()
    drawCircleHandler, drawKDEHandler, drawMainContourHandler, drawContourHandler, drawWingletsHandler = drawHandler.init()

    dots = myDB.getDots(fieldsName)['dots']
    modifiedDots, clusterInfo, globalMaxDensityPoints, proximityPoints = myKdeHandler.computeKDE(dots)
    drawHandler.getInfo(clusterInfo['clusters'], globalMaxDensityPoints, proximityPoints)
    drawCircleHandler.drawCircleTest(clusterInfo['clusters'], globalMaxDensityPoints)
    # drawCircleHandler.drawProximityCircle(proximityPoints)
    # drawCircleHandler.drawCommonFateCircle(clusterInfo['clusters'])
    # drawKDEHandler.drawKDEMap(clusterInfo['clusters'])
    drawContourHandler.drawContour(clusterInfo['clusters'])
    drawMainContourHandler.drawMainContour(clusterInfo['clusters'])
    print('*******')
    curClusterInfo, mapClassIdDotIndexStroke, liMainContour = wingletsStepHandler.startDrawWinglets(dots, clusterInfo)
    drawMainContourHandler.drawTwoPointLine(curClusterInfo, mapClassIdDotIndexStroke)
    drawWingletsHandler.generateWings(curClusterInfo, mapClassIdDotIndexStroke)
    drawHandler.endDraw()

# cv.pack()
# root.mainloop()

