import math;
class getGeoInfo():
    g_strokeMaxLength = 100
    g_strokeMinLength = 0

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
    
    def getDis(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) * (pos1[0] - pos2[0]) + (pos1[1] - pos2[1]) * (pos1[1] - pos2[1]))
    
    def getPosinLine(self, pos1, pos2, curLen):
        lineDis = self.getDis(pos1, pos2)
        delta = curLen / lineDis
        return [pos1[0] + (pos2[0] - pos1[0]) * delta, pos1[1] + (pos2[1] - pos1[1]) * delta]
    
    def getLengthbyContourIndex(self, curIsoIndex):
        curMaxIsoIndex = 20
        curMinIsoIndex = 0
        # ? 定义在geooperate.js第279行
        curMaxLength = self.g_strokeMaxLength
        curMinLength = self.g_strokeMinLength

        return curMinLength + (curMaxLength - curMinLength) * (curMaxIsoIndex - curIsoIndex) / (curMaxIsoIndex - curMinIsoIndex)

    def getLineXYatPercent(self, startPt, endPt, percent):
        # if(startPt.x):
        dx = endPt['x'] - startPt['x']
        dy = endPt['y'] - startPt['y']
        X = startPt['x'] + dx*percent
        Y = startPt['y'] + dy*percent

        return {'x': X, 'y': Y}
     
