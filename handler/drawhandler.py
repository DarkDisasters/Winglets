# import tkinter;
# import tkinter.messagebox;

# from tkinter import *;

import tkinter
import tkinter.messagebox

from tkinter import *

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sns.set(style="ticks")


root = Tk();
cv = Canvas(root, width=1200, height=1200, bg='white')



class ColorMap():
    colorDict = {'1': 'red', '2': 'blue', '3':'pink', '4': 'orange', '5':'purple', '6':'indigo'}
    colorList = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']

class DrawCircle():
    def drawCircleTest(self, clusterInfo):
        print('drawCircle')
        # print('dots', dots)
        colorRadius = 5
        for i in range(len(clusterInfo)):
            curClassIdDots = clusterInfo[i]['transferDots']
            curClassId = clusterInfo[i]['classId']
            for j in range(len(curClassIdDots)):
                curClassIdCurDot = curClassIdDots[j]
                # 用tkinter画圆形
                cv.create_oval(curClassIdCurDot[0]-colorRadius, curClassIdCurDot[1]-colorRadius, curClassIdCurDot[0]+colorRadius, curClassIdCurDot[1]+colorRadius, fill=globalColorHandler.colorDict[curClassId])

class DrawKDE():
    def drawKDEMap(self, clusterInfo):
        print('drawKDE')
        liClusterInfo = clusterInfo['clusters']
        for i in range(len(liClusterInfo)):
            # curDensityX = liClusterInfo[i]['m12'][0]
            # curDensityY = liClusterInfo[i]['m12'][1]
            # sns.kdeplot(curDensityX, curDensityY, shade=True,color='r')
            fig, ax = plt.subplots(num=100)
            curDensity = liClusterInfo[i]['density']
            im = ax.imshow(np.rot90(curDensity), cmap='Blues', extent=[0, 800, 0, 800])
            plt.show()

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
            contourLine = cv.create_line(curContourDotArr, fill=globalColorHandler.colorDict[curClassId])


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
            line = cv.create_line(curCurveDotArr, fill='black')

class DrawAllHandler():
    def init(self):
        drawCircleHandler = DrawCircle()
        drawKDEHandler = DrawKDE()
        drawContourHandler = DrawContour()
        drawWingletsHandler = DrawWinglets()
        return drawCircleHandler, drawKDEHandler, drawContourHandler, drawWingletsHandler
    
    def endDraw(self):
        cv.pack()
        root.mainloop()

globalColorHandler = ColorMap()


