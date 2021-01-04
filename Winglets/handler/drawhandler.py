# import tkinter;
# import tkinter.messagebox;

# from tkinter import *;

import tkinter
import tkinter.messagebox

from tkinter import *

import numpy as np
import pandas as pd
from threading import Timer;
import time;
import math;

from .buttonhandler import ButtonOperation


buttonOpeInstance = ButtonOperation()

root = Tk();
root.geometry('1300x1300')
# root.minsize(width=400, height=200)
root.resizable(1, 1)

root.config(bg="white")
# root.attributes('alpha', 0.65)
# root.attributes('-topmost', 1)


cv = Canvas(root, width=1000, height=1000, bg='white', scrollregion=(-50, -50, 950, 950))





class ColorMap():
    colorDict = {}
    # {'1': 'red', '2': 'blue', '3':'pink', '4': 'orange', '5':'purple', '6':'indigo', '7': 'brown', '8': 'green', '9': 'yellow'}
    colorList = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']
    def __init__(self, colorArr, data):
        # if type == 'list':
        #     for i in range(len(colorArr)):
        #         self.colorDict[i] = colorArr[i]
        # elif type == 'dict':
        count = 0
        for classId in data.keys():
            self.colorDict[classId] = colorArr[count]
            count += 1 

globalColorHandler = None

class DrawCircle():
    originCircleInfoArr = []
    colorRadius = 3.5
    commonFateData = []
    commonFateTimerArr = []
    commonFateGlobalInterval = 5
    globalMaxDensityPointsArr = []

    def drawProximityCircle(self, proximityPointsArr):
        print('drawCircle')
        # print('dots', dots)
        # self.globalMaxDensityPointsArr = globalMaxDensityPoints
        for i in range(len(proximityPointsArr)):
            curClassIdDots = proximityPointsArr[i]['curClassProximityPoints']
            curClassId = proximityPointsArr[i]['classId']

            for j in range(len(curClassIdDots)):
                curClassIdCurDot = curClassIdDots[j]
                # 用tkinter画圆形
                curCircle = cv.create_oval(curClassIdCurDot[0]-self.colorRadius, curClassIdCurDot[1]-self.colorRadius, curClassIdCurDot[0]+self.colorRadius, curClassIdCurDot[1]+self.colorRadius, tags="proximityDot",fill=globalColorHandler.colorDict[curClassId])
    
    def drawCircleTest(self, clusterInfo, globalMaxDensityPoints):
        print('drawCircle')
        # print('globalColorHandler', globalColorHandler.colorDict)
        # print('dots', dots)
        self.globalMaxDensityPointsArr = globalMaxDensityPoints
        for i in range(len(clusterInfo)):
            curClassCircleArr = []
            curClassCircleDict = {}

            curClassIdDots = clusterInfo[i]['transferDots']
            curClassId = clusterInfo[i]['classId']
            
            curClassCircleDict['classId'] = curClassId

            for j in range(len(curClassIdDots)):
                curClassIdCurDot = curClassIdDots[j]
                # 用tkinter画圆形
                curCircle = cv.create_oval(curClassIdCurDot[0]-self.colorRadius, curClassIdCurDot[1]-self.colorRadius, curClassIdCurDot[0]+self.colorRadius, curClassIdCurDot[1]+self.colorRadius, tags="originDot",fill=globalColorHandler.colorDict[curClassId])
                curClassCircleArr.append(curCircle)
            curClassCircleDict['originCircle'] = curClassCircleArr
            self.originCircleInfoArr.append(curClassCircleDict)

    def commonFateControlFunc(self):
        print('test')
        for i in range(len(self.commonFateData)):
            curClassId = self.commonFateData[i]['classId']
            curDot = self.commonFateData[i]['commonFateDot']
            
            curTimer = self.commonFateTimerArr[i]

            

    def commonFateTimerFunc(self, curDataIndex, curCount):
        curCommonFateData = self.commonFateData[curDataIndex]['commonFateDot']
        isPlus = True
        
        if curCount > 4:
            isPlus = False
        elif curCount <= 1:
            isPlus = True
        
        # curTimer = Timer(5, self.commonFateTimerFunc, (, curCount))

        if isPlus:
            curCount += 1
        else:
            curCount -= 1
        
        # curTimer.start()

    def drawCommonFateCircleByPointAlone(self, clusterInfo):
        print('common fate effect')
        print('globalMaxDensityPoints', self.globalMaxDensityPointsArr)

        cycleCount = 60
        # cycleCount = 30
        moveMaxDistance = 50
        everyDistance = moveMaxDistance / cycleCount

        for i in range(len(clusterInfo)):
            curCommonFateDict = {}
            
            curTimer = Timer(5, self.commonFateTimerFunc, (i, 1))
            self.commonFateTimerArr.append(curTimer)

            curClassIdDots = clusterInfo[i]['transferDots']
            curClassId = clusterInfo[i]['classId']
            curCentroid = clusterInfo[i]['centroid']
            curMaxDensityPoints = clusterInfo[i]['maxDensityPoints']

            centroidCircleRadius = self.colorRadius + 3
            # cv.create_oval(curCentroid[0]-centroidCircleRadius, curCentroid[1]-centroidCircleRadius, curCentroid[0]+centroidCircleRadius, curCentroid[1]+centroidCircleRadius, tags="centroid",fill='black')

            curCommonFateDict['classId'] = clusterInfo[i]['classId']
            curCommonFateDict['commonFateDot'] = []
            curCommonFateDict['curVector'] = []

            # curMaxDensityPoint = curMaxDensityPoints[math.floor(len(curMaxDensityPoints) / 2)]
            curMaxDensityPoint = self.globalMaxDensityPointsArr[i]
            
            curVector = [(curMaxDensityPoint[0] - curCentroid[0]), (curMaxDensityPoint[1] - curCentroid[1])]
            # curVector = [(curCentroid[0] - curClassIdDots[j][0]), (curCentroid[1] - curClassIdDots[j][0])]
            
            # curCommonFateDot = [[curClassIdDots[j][0], curClassIdDots[j][1]], [curVector[0] + curClassIdDots[j][0], curVector[1] + curClassIdDots[j][1]]]
            # for k in range(4):
            #     curCommonFateDot.append([curVector[0] / (4-j), curVector[1] / (4-j)])
            if abs(curVector[0]) > abs(curVector[1]):
                base = curVector[0] / moveMaxDistance
                curVector[0] /= base
                curVector[1] /= base
            else:
                base = curVector[1] / moveMaxDistance
                curVector[0] /= base
                curVector[1] /= base
            
            self.commonFateData.append(curVector)

            # 数据举例
            # [{  'classId':1, 
            #     'commonFateDot':[
            #                         [
            #                             [dot1Interpolate1X,dot1Interpolate1Y], 
            #                             [dot1Interpolate2X,dot1Interpolate2Y], 
            #                             [dot1Interpolate3X,dot1Interpolate3Y]
            #                         ],
            #                         [
            #                             [dot2Interpolate1X,dot2Interpolate1Y], 
            #                             [dot2Interpolate2X,dot2Interpolate2Y], 
            #                             [dot2Interpolate3X,dot2Interpolate3Y]
            #                         ],
            #                         ...
            #                     ]
            #  }, 
            #  {'classId':5, 'commonFateDot': []},
            #  ...
            # ]
            # for j in range(len(curClassIdDots)):
            #     curCommonFateDot = []
                # curVector = [(curClassIdDots[j][0] - curCentroid[0]), (curClassIdDots[j][1] - curCentroid[1])]
                # # curVector = [(curCentroid[0] - curClassIdDots[j][0]), (curCentroid[1] - curClassIdDots[j][0])]
                
                # # curCommonFateDot = [[curClassIdDots[j][0], curClassIdDots[j][1]], [curVector[0] + curClassIdDots[j][0], curVector[1] + curClassIdDots[j][1]]]
                # # for k in range(4):
                # #     curCommonFateDot.append([curVector[0] / (4-j), curVector[1] / (4-j)])
                # if abs(curVector[0]) > abs(curVector[1]):
                #     base = curVector[0] / moveMaxDistance
                #     curVector[0] /= base
                #     curVector[1] /= base
                # else:
                #     base = curVector[1] / moveMaxDistance
                #     curVector[0] /= base
                #     curVector[1] /= base
            
                # for k in range(cycleCount):
                #     # if i == 0 and j == 0 and k == 10:
                #     #     print('curClassIdDots[j][0] - curCentroid[0]', curClassIdDots[j][0] - curCentroid[0])
                #     #     print('curVector[0]', curVector[0])
                #     #     print('test', curVector[0] / cycleCount * (k+1)*everyDistance)
                #     curCommonFateDot.append([curClassIdDots[j][0] + (k+1) * curVector[0] / cycleCount, curClassIdDots[j][1] + (k+1) * curVector[1] / cycleCount])
                # curCommonFateDict['commonFateDot'].append(curCommonFateDot)
                # curCommonFateDict['curVector'].append(curVector)
            # self.commonFateData.append(curCommonFateDict)
         
        for i in range(cycleCount):
            for j in range(len(self.commonFateData)):
                # curCommonFateClassId = self.commonFateData[j]['classId']
                # curCommonFateDots = self.commonFateData[j]['commonFateDot']
                curCommonFateDotVector = self.commonFateData[j]
                curOriginCircle = self.originCircleInfoArr[j]['originCircle']


                for k in range(len(curOriginCircle)):
                    # curCommonFateDotVector = self.commonFateData[j]['curVector'][k]
                    cv.move(curOriginCircle[k], curCommonFateDotVector[0]/cycleCount, curCommonFateDotVector[1]/cycleCount)
                    # if i == 0:
                    #     # ?有点问题,暂时以continue跳过这个过程
                    #     continue
                    #     # print('curOriginCircle[k]', curOriginCircle[k])
                    #     # print('curCommonFateDots[k]', curCommonFateDots[k])
                    #     print("clusterInfo[j]['transferDots'][k]", clusterInfo[j]['transferDots'][k])
                    #     cv.move(curOriginCircle[k], curCommonFateDots[k][i][0]-clusterInfo[j]['transferDots'][k][0], curCommonFateDots[k][i][1]-clusterInfo[j]['transferDots'][k][1])
                    # else:
                    #     # print('curCommonFateDots[k][0]', curCommonFateDots[k][0])
                    #     cv.move(curOriginCircle[k], curCommonFateDots[k][i][0] - curCommonFateDots[k][i-1][0], curCommonFateDots[k][i][1] - curCommonFateDots[k][i-1][1])
            cv.update()
            # time.sleep(0.05)
            time.sleep(0.025)
        # self.commonFateControlFunc()

    

    def drawCommonFateCircle(self, clusterInfo):
        print('common fate effect')
        print('globalMaxDensityPoints', self.globalMaxDensityPointsArr)

        cycleCount = 60
        # cycleCount = 30
        moveMaxDistance = 50
        everyDistance = moveMaxDistance / cycleCount

        for i in range(len(clusterInfo)):
            curCommonFateDict = {}
            
            curTimer = Timer(5, self.commonFateTimerFunc, (i, 1))
            self.commonFateTimerArr.append(curTimer)

            curClassIdDots = clusterInfo[i]['transferDots']
            curClassId = clusterInfo[i]['classId']
            curCentroid = clusterInfo[i]['centroid']
            curMaxDensityPoints = clusterInfo[i]['maxDensityPoints']

            centroidCircleRadius = self.colorRadius + 3
            # cv.create_oval(curCentroid[0]-centroidCircleRadius, curCentroid[1]-centroidCircleRadius, curCentroid[0]+centroidCircleRadius, curCentroid[1]+centroidCircleRadius, tags="centroid",fill='black')

            curCommonFateDict['classId'] = clusterInfo[i]['classId']
            curCommonFateDict['commonFateDot'] = []
            curCommonFateDict['curVector'] = []

            # curMaxDensityPoint = curMaxDensityPoints[math.floor(len(curMaxDensityPoints) / 2)]
            curMaxDensityPoint = self.globalMaxDensityPointsArr[i]
            
            curVector = [(curMaxDensityPoint[0] - curCentroid[0]), (curMaxDensityPoint[1] - curCentroid[1])]
            # curVector = [(curCentroid[0] - curClassIdDots[j][0]), (curCentroid[1] - curClassIdDots[j][0])]
            
            # curCommonFateDot = [[curClassIdDots[j][0], curClassIdDots[j][1]], [curVector[0] + curClassIdDots[j][0], curVector[1] + curClassIdDots[j][1]]]
            # for k in range(4):
            #     curCommonFateDot.append([curVector[0] / (4-j), curVector[1] / (4-j)])
            if abs(curVector[0]) > abs(curVector[1]):
                base = curVector[0] / moveMaxDistance
                curVector[0] /= base
                curVector[1] /= base
            else:
                base = curVector[1] / moveMaxDistance
                curVector[0] /= base
                curVector[1] /= base
            
            self.commonFateData.append(curVector)

            # 数据举例
            # [{  'classId':1, 
            #     'commonFateDot':[
            #                         [
            #                             [dot1Interpolate1X,dot1Interpolate1Y], 
            #                             [dot1Interpolate2X,dot1Interpolate2Y], 
            #                             [dot1Interpolate3X,dot1Interpolate3Y]
            #                         ],
            #                         [
            #                             [dot2Interpolate1X,dot2Interpolate1Y], 
            #                             [dot2Interpolate2X,dot2Interpolate2Y], 
            #                             [dot2Interpolate3X,dot2Interpolate3Y]
            #                         ],
            #                         ...
            #                     ]
            #  }, 
            #  {'classId':5, 'commonFateDot': []},
            #  ...
            # ]
            # for j in range(len(curClassIdDots)):
            #     curCommonFateDot = []
                # curVector = [(curClassIdDots[j][0] - curCentroid[0]), (curClassIdDots[j][1] - curCentroid[1])]
                # # curVector = [(curCentroid[0] - curClassIdDots[j][0]), (curCentroid[1] - curClassIdDots[j][0])]
                
                # # curCommonFateDot = [[curClassIdDots[j][0], curClassIdDots[j][1]], [curVector[0] + curClassIdDots[j][0], curVector[1] + curClassIdDots[j][1]]]
                # # for k in range(4):
                # #     curCommonFateDot.append([curVector[0] / (4-j), curVector[1] / (4-j)])
                # if abs(curVector[0]) > abs(curVector[1]):
                #     base = curVector[0] / moveMaxDistance
                #     curVector[0] /= base
                #     curVector[1] /= base
                # else:
                #     base = curVector[1] / moveMaxDistance
                #     curVector[0] /= base
                #     curVector[1] /= base
            
                # for k in range(cycleCount):
                #     # if i == 0 and j == 0 and k == 10:
                #     #     print('curClassIdDots[j][0] - curCentroid[0]', curClassIdDots[j][0] - curCentroid[0])
                #     #     print('curVector[0]', curVector[0])
                #     #     print('test', curVector[0] / cycleCount * (k+1)*everyDistance)
                #     curCommonFateDot.append([curClassIdDots[j][0] + (k+1) * curVector[0] / cycleCount, curClassIdDots[j][1] + (k+1) * curVector[1] / cycleCount])
                # curCommonFateDict['commonFateDot'].append(curCommonFateDot)
                # curCommonFateDict['curVector'].append(curVector)
            # self.commonFateData.append(curCommonFateDict)
         
        for i in range(cycleCount):
            for j in range(len(self.commonFateData)):
                # curCommonFateClassId = self.commonFateData[j]['classId']
                # curCommonFateDots = self.commonFateData[j]['commonFateDot']
                curCommonFateDotVector = self.commonFateData[j]
                curOriginCircle = self.originCircleInfoArr[j]['originCircle']
                

                for k in range(len(curOriginCircle)):
                    # curCommonFateDotVector = self.commonFateData[j]['curVector'][k]
                    cv.move(curOriginCircle[k], curCommonFateDotVector[0]/cycleCount, curCommonFateDotVector[1]/cycleCount)
                    # if i == 0:
                    #     # ?有点问题,暂时以continue跳过这个过程
                    #     continue
                    #     # print('curOriginCircle[k]', curOriginCircle[k])
                    #     # print('curCommonFateDots[k]', curCommonFateDots[k])
                    #     print("clusterInfo[j]['transferDots'][k]", clusterInfo[j]['transferDots'][k])
                    #     cv.move(curOriginCircle[k], curCommonFateDots[k][i][0]-clusterInfo[j]['transferDots'][k][0], curCommonFateDots[k][i][1]-clusterInfo[j]['transferDots'][k][1])
                    # else:
                    #     # print('curCommonFateDots[k][0]', curCommonFateDots[k][0])
                    #     cv.move(curOriginCircle[k], curCommonFateDots[k][i][0] - curCommonFateDots[k][i-1][0], curCommonFateDots[k][i][1] - curCommonFateDots[k][i-1][1])
            cv.update()
            # time.sleep(0.05)
            time.sleep(0.025)
        # self.commonFateControlFunc()


class DrawKDE():
    def drawKDEMap(self, clusterInfo):
        print('drawKDE')
        # liClusterInfo = clusterInfo['clusters']
        # for i in range(len(liClusterInfo)):
        #     # curDensityX = liClusterInfo[i]['m12'][0]
        #     # curDensityY = liClusterInfo[i]['m12'][1]
        #     # sns.kdeplot(curDensityX, curDensityY, shade=True,color='r')
        #     fig, ax = plt.subplots(num=100)
        #     curDensity = liClusterInfo[i]['density']
        #     im = ax.imshow(np.rot90(curDensity), cmap='Blues', extent=[0, 800, 0, 800])
        #     plt.show()

class DrawMainContour():
    def drawMainContour(self, clusterInfo):
        print('draw maincontour')
        for i in range(len(clusterInfo)):
            curMainContour = clusterInfo[i]['maincontour']
            curClassId = clusterInfo[i]['classId']
            curMainContourDotArr = []
            for p in range(len(curMainContour)):
                curMainContourDotArr.append(curMainContour[p][0])
                curMainContourDotArr.append(curMainContour[p][1])
            mainContourLine = cv.create_line(curMainContourDotArr, fill='orange', width=3, state="hidden", tags="mainContourLine")

    def drawTwoPointLine(self, clusterInfo, mapClassIdDotIndexStroke):
        colorRadius = 4
        for i in range(len(clusterInfo)):
            curClassId = clusterInfo[i]['classId']
            liDots = clusterInfo[i]['dots']
            mapIndexStrokeInfo = mapClassIdDotIndexStroke[curClassId]
            
            for j in range(len(liDots)):
                curOriginPos = liDots[j]
                curIntersectionPos = mapIndexStrokeInfo[j]['intersection']
                # curIntersectionPos = mapClassIdDotIndexStroke[curClassId]['intersection']
                # curOriginPos = mapClassIdDotIndexStroke[curClassId]['originDot']
                curLineArr = [curOriginPos, curIntersectionPos]
                line = cv.create_line(curLineArr, fill='green', width=3, state="hidden", tags="twoPointLine")
                circle = cv.create_oval(curIntersectionPos[0]-colorRadius, curIntersectionPos[1]-colorRadius, curIntersectionPos[0]+colorRadius, curIntersectionPos[1]+colorRadius, state="hidden", fill='green', tags="intersectionPos")


class DrawContour():
    print('drawContour')
    def drawContour(self, clusterInfo):
        for i in range(len(clusterInfo)):
            curContour = clusterInfo[i]['contours']
            curClassId = clusterInfo[i]['classId']
            curContourDotArr = []
            for isovalue in curContour:
                for p in range(len(curContour[isovalue][0])):
                    curContourDotArr.append(curContour[isovalue][0][p][0])
                    curContourDotArr.append(curContour[isovalue][0][p][1])
            contourLine = cv.create_line(curContourDotArr, fill=globalColorHandler.colorDict[curClassId], state="hidden", tags="contourLine")

class DrawWinglets():
    print('drawWinglets')

    def generateWings(self, clusterInfo, mapClassIdDotIndexStroke):
        for i in range(len(clusterInfo)):
            curClassId = clusterInfo[i]['classId']
            liDots = clusterInfo[i]['dots']
            liContour_interpolate = clusterInfo[i]['interpolatecontours']
            mapIndexCurve = mapClassIdDotIndexStroke[curClassId]
            classColor = 'black'
            self.addDotCurves_svg(curClassId, liDots, mapIndexCurve, classColor)

    def addDotCurves_svg(self, curClassId, dots, mapIndexCurve, strokeColr):
        for i in range(len(dots)):
            curCurve = mapIndexCurve[i]['curve']
            curCurveDotArr = []
            for j in range(len(curCurve)):
                curCurveDotArr.append(curCurve[j][0])
                curCurveDotArr.append(curCurve[j][1])
            line = cv.create_line(curCurveDotArr, fill=globalColorHandler.colorDict[curClassId], width=1.8, tags="wingletsLine")
        print('Draw Winglets Done')

class DrawAllHandler():
    commonFateButton = None
    intersectionPosButton = None
    mainContourButton = None
    twoPointLineButton = None
    contourButton = None 
    wingletsButton = None 
    testClusterInfo = []
    testCircleHander = None
    maxDensityPointsArr = []
    proximityPointsArr = []
    isCommonFateStart = False
    notCommonFateAndProximity = True
    isProximityStart = False
    clickIntervalOk = True

    def init(self, onlyWinglets, onlyCircle, onlyCommonFate, onlyProximity):
        self.testCircleHander = drawCircleHandler = DrawCircle()
        self.initButton(onlyWinglets, onlyCircle, onlyCommonFate, onlyProximity)
        drawKDEHandler = DrawKDE()
        drawMainContourHandler = DrawMainContour()
        drawContourHandler = DrawContour()
        drawWingletsHandler = DrawWinglets()
        return drawCircleHandler, drawKDEHandler, drawMainContourHandler, drawContourHandler, drawWingletsHandler

    def initGlobalColor(self, colorArray, data):
        global globalColorHandler
        globalColorHandler = ColorMap(colorArray, data)
        # print('globalColorHandler' ,globalColorHandler.colorDict)

    def initButton(self, onlyWinglets, onlyCircle, onlyCommonFate, onlyProximity):
        if onlyCircle:
            return 0
        if onlyCommonFate:
            self.commonFateButton = Button(root, text="commonFate", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: self.startCommonFate())
            self.commonFateButton.place(x=1100, y=500, width=100)
            return 0
        elif onlyProximity:
            self.proximityButton = Button(root, text="proximity", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: self.startProximity())
            self.proximityButton.place(x=1100, y=500, width=100)
            return 0
        elif onlyWinglets:
            self.mainContourButton = Button(root, text="mainContour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'mainContourLine'))
            self.twoPointLineButton = Button(root, text="twoPointLine", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'twoPointLine'))
            self.contourButton = Button(root, text="Contour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'contourLine'))
            self.intersectionPosButton = Button(root, text="intersectionPos", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'intersectionPos'))
            self.wingletsButton = Button(root, text="Winglets", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'wingletsLine'))
            
            self.mainContourButton.place(x=1025, y=450, width=100)
            self.twoPointLineButton.place(x=1150, y=450, width=100)
            self.contourButton.place(x=1025, y=500, width=70)
            self.intersectionPosButton.place(x=1110, y=500, width=100)
            self.wingletsButton.place(x=1225, y=500, width=70)
            return 0

        self.proximityButton = Button(root, text="proximity", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: self.startProximity())
        self.commonFateButton = Button(root, text="commonFate", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: self.startCommonFate())
        self.intersectionPosButton = Button(root, text="intersectionPos", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'intersectionPos'))
        self.mainContourButton = Button(root, text="mainContour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'mainContourLine'))
        self.twoPointLineButton = Button(root, text="twoPointLine", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'twoPointLine'))
        self.contourButton = Button(root, text="Contour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'contourLine'))
        self.wingletsButton = Button(root, text="Winglets", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'wingletsLine'))
        
        self.proximityButton.place(x=1025, y=350, width=100)
        self.commonFateButton.place(x=1025, y=400, width=100)
        self.intersectionPosButton.place(x=1150, y=400, width=100)
        self.mainContourButton.place(x=1025, y=450, width=100)
        self.twoPointLineButton.place(x=1150, y=450, width=100)
        self.contourButton.place(x=1025, y=500, width=70)
        self.wingletsButton.place(x=1110, y=500, width=70)

    def getInfo(self, clusterInfo, maxDensityPointsArr, proximityPointsArr):
        self.testClusterInfo = clusterInfo
        self.maxDensityPointsArr = maxDensityPointsArr
        self.proximityPointsArr = proximityPointsArr
    
    def startCommonFate(self):
        if not self.clickIntervalOk:
            print('click interval not ok, program is running, please wait')
            return 0
        # ? 先点proximity再点commonFate,commonFate函数运行但是没动画
        if not self.isCommonFateStart and self.notCommonFateAndProximity:
            print('commonFate state', self.isCommonFateStart)
            self.clickIntervalOk = False
            self.testCircleHander.drawCommonFateCircle(self.testClusterInfo)
            self.isCommonFateStart = True
            self.notCommonFateAndProximity = False
            self.isProximityStart = False
            time.sleep(2)
            self.clickIntervalOk = True
            print('clickIntervalOk')
        elif not self.notCommonFateAndProximity and self.isCommonFateStart:
            print('commonFate state', self.isCommonFateStart)
            self.clickIntervalOk = False
            cv.delete('originDot')
            cv.delete('proximityDot')
            self.testCircleHander.drawCircleTest(self.testClusterInfo, self.maxDensityPointsArr)
            self.isCommonFateStart = False
            self.notCommonFateAndProximity = True
            self.isProximityStart = False
            time.sleep(2)
            self.clickIntervalOk = True
            print('clickIntervalOk')
        
    def startProximity(self):
        if not self.clickIntervalOk:
            print('click interval not ok, program is running, please wait')
            return 0

        if not self.notCommonFateAndProximity and self.isProximityStart:
            print('proximity state', self.isProximityStart)
            self.clickIntervalOk = False
            cv.delete('proximityDot')
            self.testCircleHander.drawCircleTest(self.testClusterInfo, self.maxDensityPointsArr)
            self.isCommonFateStart = False
            self.notCommonFateAndProximity = True
            self.isProximityStart = False
            time.sleep(2)
            self.clickIntervalOk = True
            print('clickIntervalOk')
        elif not self.isProximityStart and self.notCommonFateAndProximity:
            print('commonFate state', self.isCommonFateStart)
            self.clickIntervalOk = False
            cv.delete('originDot')
            self.testCircleHander.drawProximityCircle(self.proximityPointsArr)
            self.isCommonFateStart = False
            self.notCommonFateAndProximity = False 
            self.isProximityStart = True
            time.sleep(2)
            self.clickIntervalOk = True
            print('clickIntervalOk')

    def endDraw(self):
        # self.contourButton.pack(side=RIGHT)
        # self.wingletsButton.pack(side=RIGHT)
        
        cv.place(x=0, y=0)
        root.mainloop()




