class Path():
    _closed = False
    _segments = []
    _version = 0

    _segments.length = 0
    _segmentSelection = 0
    _curves = None

    def initialize(self, arg):
        segments = arg

        if segments and (len(segments) > 0):
            self.setSegments(segments)

    def setSegments(self, segments):
        fullySelected = self.isFullySelected()
        length = segments and len(segments)
        
        # ? this._segments.length = 0;
        # len(self._segments) = 0
        self._segments = []
        self._segmentSelection = 0
        self._curves = None
        if length:
            last = segments[length - 1]
            if type(last) == bool:
                self.setClosed(last)
                length -= 1
            # self._add()
            
    def setClosed(self, closed):
        # if self._closed != (closed = not not closed):
        closed = not not closed
        if self._closed != closed:
            self._closed = closed
            if self._curves:
                length = self._countCurves()
                self._curves = self._curves[0: length]
                if closed:
                    self._curves[length - 1] = new Curve(self, )

    def _countCurves(self):
        length = len(self._segments)
        if not self._closed and length > 0:
            return length - 1
        else:
            return length

    def isFullySelected(self):
        length = len(self._segments)
        # return self.isSelected() and length > 0 and self._segmentSelection == length * 7
        return length > 0 and self._segmentSelection == length * 7