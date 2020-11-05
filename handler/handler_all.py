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
    dots = myDB.getDots(fieldsName)['dots']
    modifiedDots, clusterInfo = myKdeHandler.computeKDE(dots)
    print('*******')
    wingletsStepHandler.startDrawWinglets(dots, clusterInfo)
    # wingletsStepHandler.computeDisMatrix(dots)
    # wingletsStepHandler.computeSilhouette(clusterInfo['clusters'])
    # print(modifiedDots)
    drawHandler = DrawAllHandler()
    drawCircleHandler, drawContourHandler, drawWingletsHandler = drawHandler.init()
    drawCircleHandler.drawCircleTest(modifiedDots)
    drawHandler.endDraw()

# cv.pack()
# root.mainloop()

