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

from handler.buttonhandler import ButtonOperation

sns.set(style="ticks")

buttonOpeInstance = ButtonOperation()

root = Tk();
root.geometry('1300x1300')
# root.minsize(width=400, height=200)
root.resizable(1, 1)

root.config(bg="white")
# root.attributes('alpha', 0.65)
# root.attributes('-topmost', 1)


cv = Canvas(root, width=1000, height=1000, bg='white')





class ColorMap():
    colorDict = {'1': 'red', '2': 'blue', '3':'pink', '4': 'orange', '5':'purple', '6':'indigo', '7': 'brown', '8': 'green', '9': 'yellow'}
    colorList = ['red', 'blue', 'pink', 'orange', 'purple', 'indigo']

globalColorHandler = ColorMap()

class DrawCircle():
    def drawCircleTest(self, clusterInfo):
        print('drawCircle')
        # print('dots', dots)
        colorRadius = 3.5
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
    intersectionPosButton = Button(root, text="intersectionPos", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'intersectionPos'))
    mainContourButton = Button(root, text="mainContour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'mainContourLine'))
    twoPointLineButton = Button(root, text="twoPointLine", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'twoPointLine'))
    contourButton = Button(root, text="Contour", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'contourLine'))
    wingletsButton = Button(root, text="Winglets", bg='white', activebackground='#F0F0F0', bd=1, relief="ridge", command = lambda: buttonOpeInstance.orihiddenElement(cv, 'wingletsLine'))

    def init(self):
        drawCircleHandler = DrawCircle()
        drawKDEHandler = DrawKDE()
        drawMainContourHandler = DrawMainContour()
        drawContourHandler = DrawContour()
        drawWingletsHandler = DrawWinglets()
        return drawCircleHandler, drawKDEHandler, drawMainContourHandler, drawContourHandler, drawWingletsHandler
    
    def endDraw(self):
        # self.contourButton.pack(side=RIGHT)
        # self.wingletsButton.pack(side=RIGHT)
        self.intersectionPosButton.place(x=1025, y=400, width=100)
        self.mainContourButton.place(x=1025, y=450, width=100)
        self.twoPointLineButton.place(x=1150, y=450, width=100)
        self.contourButton.place(x=1025, y=500, width=70)
        self.wingletsButton.place(x=1110, y=500, width=70)
        cv.place(x=0, y=0)
        root.mainloop()




