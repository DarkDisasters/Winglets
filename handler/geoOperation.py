class getGeoInfo():
    def getCentroid(self, liPos):
        centroid = [0, 0]
        if(len(liPos) < 0):
            return centroid
        for i in range(len(liPos)):
            centroid[0] += liPos[i][0]
            centroid[1] += liPos[i][1]
        centroid[0] /= len(liPos)
        centroid[1] /= len(liPos)
        return centroid
    
    def getLineXYatPercent(self, startPt, endPt, percent):
        # if(startPt.x):
        dx = endPt['x'] - startPt['x']
        dy = endPt['y'] - startPt['y']
        X = startPt['x'] + dx*percent
        Y = startPt['y'] + dy*percent

        return {'x': X, 'y': Y}
     
