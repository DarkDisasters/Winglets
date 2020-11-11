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
    drawCircleHandler, drawKDEHandler, drawContourHandler, drawWingletsHandler = drawHandler.init()

    dots = myDB.getDots(fieldsName)['dots']
    modifiedDots, clusterInfo = myKdeHandler.computeKDE(dots)
    drawCircleHandler.drawCircleTest(clusterInfo['clusters'])
    # drawKDEHandler.drawKDEMap(clusterInfo['clusters'])
    drawContourHandler.drawContour(clusterInfo['clusters'])
    print('*******')
    curClusterInfo, mapClassIdDotIndexStroke = wingletsStepHandler.startDrawWinglets(dots, clusterInfo)
    drawWingletsHandler.generateWings(curClusterInfo, mapClassIdDotIndexStroke)
    drawHandler.endDraw()

# cv.pack()
# root.mainloop()

