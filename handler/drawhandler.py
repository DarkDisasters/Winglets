# import tkinter;
# import tkinter.messagebox;

# from tkinter import *;

import tkinter
import tkinter.messagebox

from tkinter import *

root = Tk();
cv = Canvas(root, width=1200, height=1200, bg='white')



class DrawCircle():
    def drawCircleTest(self, dots):
        print('drawCircle')
        # print('dots', dots)
        colorList = ['red', 'blue', 'yellow']
        colorRadius = 5
        for i in range(len(dots)):
            curClassIdDots = dots[i]
            for j in range(len(curClassIdDots)):
                curClassIdCurDot = curClassIdDots[j]
                # 用tkinter画圆形
                cv.create_oval(curClassIdCurDot[0]-colorRadius, curClassIdCurDot[1]-colorRadius, curClassIdCurDot[0]+colorRadius, curClassIdCurDot[1]+colorRadius, fill=colorList[i])


class DrawContour():
    print('drawContour')

class DrawWinglets():
    print('drawWinglets')

class DrawAllHandler():
    def init(self):
        drawCircleHandler = DrawCircle()
        drawContourHandler = DrawContour()
        drawWingletsHandler = DrawWinglets()
        return drawCircleHandler, drawContourHandler, drawWingletsHandler
    
    def endDraw(self):
        cv.pack()
        root.mainloop()




