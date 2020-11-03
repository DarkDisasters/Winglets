import math;
from geoOperation import getGeoInfo;
from shapely.geometry import LineString;
from shapely.geometry import Point;
from shapely.geometry import Polygon;

class DistanceOperation():
    def getDifClassDotDistance(self, dot1, dot2):
        return math.sqrt((dot1[0] - dot2[0])*(dot1[0] - dot2[0]) + (dot1[1] - dot2[1])*(dot1[1] - dot2[1]))

class WingletsStepHandler():
    m_mapDisMatrix = {}
    m_mapClassIdDotIndexSihouttle = {}
    m_mapClassIdMaxMinSI = {}
    m_mapClassIdDotIndexSensitivity = {}

    geoInstance = getGeoInfo()

    # 不知道有啥用
    def sortIsoValue(self, mapIsoValueContour):
        liSortedIsoValueStr = []
        liIsoValueStr = mapIsoValueContour.keys()
        liNewIsoValue = []

        for i in range(len(liIsoValueStr)):
            liNewIsoValue.append(int(liIsoValueStr[i]))
        liNewIsoValue.sort()

        for i in range(len(liNewIsoValue)):
            curIsoValueNum = liNewIsoValue[i]
            for j in range(len(liIsoValueStr)):
                isoValueTmp = int(liIsoValueStr[j])
                if(abs(curIsoValueNum - isoValueTmp) < 1e-6):
                    liSortedIsoValueStr.append(liIsoValueStr[j])
        return liSortedIsoValueStr

    def getRadialIntersection(self, pos1, pos2, contour):
        centroidPos = Point(pos1[0], pos1[1])
        # ？1500 不知道是干什么的
        dataPos = Point(1500 * pos2[0] - 1500 * pos1[0], 1500 * pos2[1] - 1500 * pos1[1])
        centroidAlongLinePath = LineString(centroidPos, dataPos)

        contourPathPoints = []
        for i in range(len(contour)):
            contourPathPoints.append(Point(contour[i][0], contour[i][1]))
        # 因为shapely没有添加的api，所以将点放在数组里使用Polygon一次性生成polygon
        contourPath = Polygon(contourPathPoints)

        # 通过shapely的intersection获取到LineString和Polygon的交集，应该是一条lineString，可以用coords来获取交集的点
        # 如果交集为一个线段，一个点为交点，一个点为线段中的一个点，一般是第一个元素
        liIntersectionsCoords = list(contourPath.intersection(centroidAlongLinePath).coords)

        #chose the closest one
        minDistance = 1e6
        minIndex = -1
        for i in range(len(liIntersectionsCoords)):
            dis_temp = math.sqrt(math.pow(liIntersectionsCoords[i][0] - pos2[0], 2) + math.pow(liIntersectionsCoords[i][1] - pos2[1], 2))
            if (dis_temp < minDistance):
                minDistance = dis_temp
                minIndex = i
        if (minIndex == -1):
            return {'pos': [], 'index': -1}    
    	
        return {
            'pos': [liIntersectionsCoords[minIndex][0], liIntersectionsCoords[minIndex][1]],
            #? intersections[minIndex].index
            'index': minIndex
        }
        



    def interpolateContourSelf(self, contour, contourNum):
        mapIndexContour = {}
        liDeformVector = []
        sampleNum = 120
        centroidPos = self.geoInstance.getCentroid(contour)
        for i in range(len(sampleNum)):
            arc = (i * 2 * math.pi) / sampleNum
            intersectResult_outer = self.getRadialIntersection(centroidPos, [centroidPos[0] + 100*math.cos(arc), centroidPos[1] + 100*math.sin(arc)], contour)
            deformVector = [centroidPos, intersectResult_outer['pos']]
            liDeformVector.append(deformVector)
            #interpolate
            for p in range(contourNum):
                perCentage = (p+1) / (contourNum + 1)
                contourPos = self.geoInstance.getLineXYatPercent({'x': deformVector[0][0], 'y': deformVector[0][1]},
                                                               {'x': deformVector[1][0], 'y': deformVector[1][1]},
                                                               perCentage)

                
                if(p not in mapIndexContour.keys()):
                    mapIndexContour[p] = [[contourPos['x'], contourPos['y']]]
                else:
                    mapIndexContour[p].append([contourPos['x'], contourPos['y']])
        return mapIndexContour

    def computeDisMatrix(self, data):
        distanceOpeInstance = DistanceOperation()
        liClusterId = list(data.keys())

        for i in range(len(liClusterId)):
            curCluster1 = liClusterId[i]
            curDots1 = data[curCluster1]
            for p in range(len(curDots1)):
                curDot1 = curDots1[p]
                for j in range(i, len(liClusterId)):
                    curCluster2 = liClusterId[j]
                    curDots2 = data[curCluster2]
                    for q in range(len(curDots2)):
                        curDot2 = curDots2[q]
                        curDistance = distanceOpeInstance.getDifClassDotDistance([curDot1['x'], curDot2['y']], [curDot2['x'], curDot2['y']])
                        self.m_mapDisMatrix[str(curCluster1) + '_' + str(p) + '-' + str(curCluster2) + '_' + str(q)] = curDistance
                        self.m_mapDisMatrix[str(curCluster2) + '_' + str(q) + '-' + str(curCluster1) + '_' + str(p)] = curDistance
    
    def computeSilhouette(self, clusterInfo):
        m_mapClassIDDotIndexSihouttle = {}
        m_mapClassIDMaxMinSI = {}

        disMatrix = self.m_mapDisMatrix
        g_Max = 1e-6
        g_Min = 1e6

        for i in range(len(clusterInfo)):
            curClusterId1 = clusterInfo[i]['classId']

            liNormalSIIndex = []
            silhoutte_min = 1e6
            silhoutte_max = 1e-6

            curLiDots1 = clusterInfo[i]['dots']
            liSilhoutteIndex = []

            for p in range(len(curLiDots1)):
                avgA = 0
                for q in range(len(curLiDots1)):
                    if((str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)) in self.m_mapDisMatrix):
                        avgA += self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)]
                    else:
                        avgA += 5
                avgA /= len(curLiDots1)
                sihoutte = 0
                avgB = 1e6
                for j in len(clusterInfo):
                    if (i == j):
                        continue
                    curClusterId2 = clusterInfo[j]['classId']
                    curLiDots2 = clusterInfo[j]['dots']
                    tempAvgB = 0
                    for k in range(len(curLiDots2)):
                        if (curClusterId1 > curClusterId2):
                            if((str(curClusterId2) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)) in self.m_mapDisMatrix == False):
                                tempAvgB += 10
                            else:
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId2) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)]
                        else:
                            if((str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(q)) in self.m_mapDisMatrix == False):
                                tempAvgB += 10
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(q)]
                    tempAvgB /= len(curLiDots2)
                    if(avgB > tempAvgB):
                        avgB = tempAvgB
                
                if(avgA < avgB):
                    sihoutte = 1 - avgA/avgB
                elif(avgA == avgB):
                    sihoutte = 0
                else:
                    sihoutte = avgB/avgA - 1
            
            liSilhoutteIndex.append(sihoutte)
            if(silhoutte_max < sihoutte):
                silhoutte_max = sihoutte;
            if(silhoutte_min > sihoutte):
                silhoutte_min = sihoutte;
            if(g_Min > sihoutte):
                g_Min = sihoutte;
            if(g_Max < sihoutte):
                g_Max = sihoutte
            
        for sihoutteIndex in range(len(liSilhoutteIndex)):
            liNormalSIIndex.append((liSilhoutteIndex[sihoutteIndex] - silhoutte_min) / (silhoutte_max - silhoutte_min))
        
        self.m_mapClassIdDotIndexSihouttle[curClusterId1] = liNormalSIIndex
        self.m_mapClassIdMaxMinSI[curClusterId1] = [silhoutte_max, silhoutte_min]
    
    def computeDotStrokes(self, clusterInfo):
        m_WingType = 'outcontour'

        for i in range(len(clusterInfo)):
            curClusterId = clusterInfo[i]['classId']
            curDots = clusterInfo[i]['dots']

            liSihoutteIndex = []
            liSensitivity = []

            if(curClusterId in self.m_mapClassIdDotIndexSihouttle.keys()):
                liSihoutteIndex = self.m_mapClassIdDotIndexSihouttle[curClusterId]
            if(curClusterId in self.m_mapClassIdDotIndexSensitivity.keys()):
                liSensitivity = self.m_mapClassIdDotIndexSensitivity[curClusterId]

            liKDE = clusterInfo[i]['density']
            mapContours = clusterInfo[i]['contours']
            mapCounts = clusterInfo[i]['counts']
            mainContour = clusterInfo[i]['maincontour']
            mainIsoValue = clusterInfo[i]['mainisovalue']

            mapMainIsoContour = {}
            mapDotIndexDeepIsoIndex = {}

            # mapIsoValueCanvasContours = self.convertContourToCanvas(mapContours)
            #不知道排序的作用
            liSortedIsoValueStr = self.sortIsoValue(mapContours)
            clusterInfo[i]['sortedIsoValue'] = liSortedIsoValueStr

            outContour = []
            # spcanvas.js第1575行有几个if判断，不知道选哪个
            outIsoValue = liSortedIsoValueStr[1]
            outContour = mapContours[outIsoValue][0]

            # 根据公共轮廓插值，并根据中心点与该点连线与contour的交集找到在contour上离该点最近的点
            mapNewIndexContours = self.interpolateContourSelf(outContour, 20)

            mapNewCanvasContours = {}
            mapNewIsoValueInnerContours = {}
            mapNewCanvasContours[outIsoValue] = [outContour]
            mapNewIsoValueInnerContours[outIsoValue] = mapNewIndexContours

            





