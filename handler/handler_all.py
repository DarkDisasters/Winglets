from handler.mongohandler import MONGODBHANDLER
from handler.kdehandler import KDEHandler

myDB = MONGODBHANDLER()
myDB.connectDB('First', 'localhost', 27017)

myKdeHandler = KDEHandler()

def outputDots(fieldsName):
    dots = myDB.getDots(fieldsName)['dots']
    returnValue = myKdeHandler.computeKDE(dots)
    # print(returnValue)

