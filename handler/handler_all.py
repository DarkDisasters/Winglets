from handler.mongohandler import MONGODBHANDLER
from handler.kdehandler import KDEHandler
from handler.drawhandler import DrawAllHandler

myDB = MONGODBHANDLER()
myDB.connectDB('First', 'localhost', 27017)

myKdeHandler = KDEHandler()
# cv = Canvas(root, bg='white')


def outputDots(fieldsName):
    dots = myDB.getDots(fieldsName)['dots']
    modifiedDots, clusterInfo = myKdeHandler.computeKDE(dots)
    print('*******')
    # print(modifiedDots)
    drawHandler = DrawAllHandler()
    drawCircleHandler, drawContourHandler, drawWingletsHandler = drawHandler.init()
    drawCircleHandler.drawCircleTest(modifiedDots)
    drawHandler.endDraw()

# cv.pack()
# root.mainloop()

