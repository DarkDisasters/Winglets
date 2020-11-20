class ButtonOperation(): 
    isIntersectionPosDisplay = False
    isMainContourDisplay = False
    isTwoPointLineState = False
    isContourDisplay = False
    isWingletsDisplay = True

    intersectionPosState = None
    mainContourState = None
    twoPointLineState = None
    contourState = None
    wingletsState = None

    def orihiddenElement(self, curCanvas, tagName):
        print('curButtonTag', tagName)

        curControlState = None
        curControlDisplay = None

        if tagName == 'intersectionPos':
            self.isIntersectionPosDisplay = not self.isIntersectionPosDisplay
            if self.isIntersectionPosDisplay:
                curControlState = 'normal'
            else:
                curControlState = 'hidden'
        elif tagName == 'mainContourLine':
            self.isMainContourDisplay = not self.isMainContourDisplay
            if self.isMainContourDisplay:
                curControlState = 'normal'
            else:
                curControlState = 'hidden'
        elif tagName == 'twoPointLine':
            self.isTwoPointLineState = not self.isTwoPointLineState
            if self.isTwoPointLineState:
                curControlState = 'normal'
            else:
                curControlState = 'hidden'
        elif tagName == 'contourLine':
            self.isContourDisplay = not self.isContourDisplay
            if self.isContourDisplay:
                curControlState = 'normal'
            else:
                curControlState = 'hidden'
        elif tagName == 'wingletsLine':
            self.isWingletsDisplay = not self.isWingletsDisplay
            if self.isWingletsDisplay:
                curControlState = 'normal'
            else:
                curControlState = 'hidden'
        
        curCanvas.itemconfig(tagName, state = curControlState)

    def mainContourButtonOpe(self, curCanvas):
        print('main contour button click')
        mainContourState = None
        self.isMainContourDisplay = not self.isMainContourDisplay
        # curCanvas.delete('contourLine')
        if self.isMainContourDisplay:
            mainContourState = 'normal'
        else: 
            mainContourState = 'hidden'
        curCanvas.itemconfig('mainContourLine', state = mainContourState)

    def contourButtonOpe(self, curCanvas):
        print('contour button click')
        contourState = None
        self.isContourDisplay = not self.isContourDisplay
        # curCanvas.delete('contourLine')
        if self.isContourDisplay:
            contourState = 'normal'
        else: 
            contourState = 'hidden'
        curCanvas.itemconfig('contourLine', state = contourState)

    
    def wingsButtonOpe(self, curCanvas):
        print('wings button click')
        wingletsState = None
        self.isWingletsDisplay = not self.isWingletsDisplay
        # curCanvas.delete('contourLine')
        if self.isWingletsDisplay:
            wingletsState = 'normal'
        else: 
            wingletsState = 'hidden'
        curCanvas.itemconfig('wingletsLine', state = wingletsState)
