import math;
from handler.geoOperation import getGeoInfo;
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
    m_drawInterContour = {}

    m_xMin = 0
    m_xMax = 0
    m_yMin = 0
    m_yMax = 0
    m_OC_PointDisToCentroid_min = 1e6
    m_OC_PointDisToCentroid_max = -1e6
    m_diff = True

    geoInstance = getGeoInfo()

    # 不知道有啥用
    def sortIsoValue(self, mapIsoValueContour):
        liSortedIsoValueStr = []
        liIsoValueStr = list(mapIsoValueContour.keys())
        # print('mapIsoValueContour', mapIsoValueContour)
        # print('liIsoValueStr', liIsoValueStr)
        liNewIsoValue = []

        for i in range(len(liIsoValueStr)):
            # liNewIsoValue.append(int(liIsoValueStr[i]))
            liNewIsoValue.append(float(liIsoValueStr[i]))
        liNewIsoValue.sort()

        for i in range(len(liNewIsoValue)):
            curIsoValueNum = liNewIsoValue[i]
            for j in range(len(liIsoValueStr)):
                # isoValueTmp = int(liIsoValueStr[j])
                isoValueTmp = float(liIsoValueStr[j])
                if(abs(curIsoValueNum - isoValueTmp) < 1e-6):
                    liSortedIsoValueStr.append(liIsoValueStr[j])
        return liSortedIsoValueStr

    def getRadialIntersection(self, pos1, pos2, contour):
        centroidPos = Point(pos1[0], pos1[1])
        # ？1500 不知道是干什么的
        dataPos = Point(1500 * pos2[0] - 1500 * pos1[0], 1500 * pos2[1] - 1500 * pos1[1])
        centroidAlongLinePath = LineString([centroidPos, dataPos])

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
        # ?补充120度的弧度的边
        for i in range(sampleNum):
            arc = (i * 2 * math.pi) / sampleNum
            # ？
            intersectResult_outer = self.getRadialIntersection(centroidPos, [centroidPos[0] + 100*math.cos(arc), centroidPos[1] + 100*math.sin(arc)], contour)
            deformVector = [centroidPos, intersectResult_outer['pos']]
            liDeformVector.append(deformVector)
            #interpolate
            #想要interpolate出contourNum个contour
            for p in range(contourNum):
                # percentage为当前的percentage，contourPos为根据当前的percentage与当前弧度生成的deformVector代表的向量所插成的点
                perCentage = (p+1) / (contourNum + 1)
                contourPos = self.geoInstance.getLineXYatPercent({'x': deformVector[0][0], 'y': deformVector[0][1]},
                                                               {'x': deformVector[1][0], 'y': deformVector[1][1]},
                                                               perCentage)

                # mapIndexContour为 {}，以p也就是contourNum遍历的index作为key，也就是第几层contour，
                # 而在不同的p层contour中append的为遍历了sampleNum次生成的不同弧度对应的contourPos。

                # 即每一个对象的key对应了该contour下sampleNum个数组，
                # deformVector：centroids与该点生成的向量1与最近的contour生成的交集，然后中心点和该交集共同作为deformVector
                # 通过循环了contourNum次，找到每个contourNum下的deformVector的点，并将这些点放置在对应的key为p的数组里面，
                # 每个p对应的数组里存放了 sampleNum个 交点
                if(p not in mapIndexContour.keys()):
                    mapIndexContour[p] = [[contourPos['x'], contourPos['y']]]
                else:
                    mapIndexContour[p].append([contourPos['x'], contourPos['y']])
        return mapIndexContour

    def getLengthBySI(self, curSI):
        return 9 + curSI * 18

    # ? spcanvas.js第3211行，有很多判断，只选取了 gestalt的
    def getLengthSpecialCase(self, curCurveLength, curSI):
        s = 8
        curveLength = s + curSI * 15
        if curveLength < s:
            curveLength = s
        return curveLength
    
    def adjustStrokesofClass(self, mapIndexStrokeBag):
        mapIndexCurve = {}
        # finer the curve and adapt to contourIndex
        liDotIndex = mapIndexStrokeBag.keys()
        m_liVisibleDotIndex = []

        for i in range(len(liDotIndex)):
            curDotIndex = liDotIndex[i]
            curveBag = mapIndexStrokeBag[curDotIndex]
            dotType = curveBag['dotType']
            sortIsovalueIndex = curveBag['sortIsovalueIndex']
            centroid = curveBag['centroid']
            liIntersectPos = curveBag['intersection']
            baseDot = curveBag['baseDot']
            curveLength = self.geoInstance.getLengthbyContourIndex(sortIsovalueIndex)
            newCurve = curveBag['dots']

            mapIndexCurve[curDotIndex] = {
                'dotType': dotType,
                'curve': newCurve,
                'level': sortIsovalueIndex,
                'centroid': centroid,
                'intersection': liIntersectPos,
                'baseDot': baseDot
            }
        return mapIndexCurve

    def preLocate(self, dots, liSihoutteIndex, liSensitivity, liKDE, 
        mapIsovalueCanvasContour, mapIsovalueInterContours, liSortedIsovalueStr):
        pointToCentroid_min = 1e6
        pointToCentroid_max = -1e6
        liIsovalue = list(mapIsovalueCanvasContour.keys())

        mapIsovalueIndexContour = {}
        mapIsovalueStrCentroids = {}

        # compute the centroid of contours
        for i in range(len(liIsovalue)):
            liContour_temp = mapIsovalueCanvasContour[liIsovalue[i]]
            for j in range(len(liContour_temp)):
                contour = liContour_temp[j]
                centroid = self.geoInstance.getCentroid(contour)
                if(liIsovalue[i] not in mapIsovalueStrCentroids.keys()):
                    mapIsovalueStrCentroids[liIsovalue[i]] = [centroid]
                else:
                    mapIsovalueStrCentroids[liIsovalue[i]].append(centroid)
        
        mapIndexCurve = {}
        mapIndexStrokeBag = {}

        step = (self.m_xMax - self.m_xMin) / 100
        mapDotIndexIsoBag = {}
        minLength = 1e6
        maxLength = -1e6

        # get the closest minisovalue_str and minContourIndex
        minLowIsoIndex = 1e6
        for i in range(len(dots)):
            curDot = dots[i]
            cellColumnIndex = math.floor((curDot[0] - self.m_xMin) / step)
            cellRowIndex = math.floor((self.m_yMax - curDot[1]) / step)
            density = liKDE[cellRowIndex * 100 + cellColumnIndex]

            # get the two boundary
            lowIsovalueStr = upperIsovalueStr = None
            lowIsoIndex = upperIsoIndex = -1
            for j in range(len(liSortedIsovalueStr) - 1):
                isovalue1 = float(liSortedIsovalueStr[j])
                isovalue2 = float(liSortedIsovalueStr[j + 1])
                if(isovalue1 <= density and isovalue2 >= density):
                    lowIsovalueStr = liSortedIsovalueStr[j]
                    upperIsovalueStr = liSortedIsovalueStr[j+1]
                    lowIsoIndex = j
                    upperIsoIndex = j+1
                    if(lowIsoIndex < minLowIsoIndex):
                        minLowIsoIndex = lowIsoIndex

            if lowIsoIndex == -1:
                lowIsoIndex = len(liSortedIsovalueStr) - 1
                lowIsovalueStr = liSortedIsovalueStr[lowIsoIndex]
                upperIsovalueStr = None
                upperIsoIndex = lowIsoIndex + 1
                if lowIsoIndex < minLowIsoIndex:
                    minLowIsoIndex = lowIsoIndex
            mapDotIndexIsoBag[i] = {
                'lowIsoIndex': lowIsoIndex,
                'lowIsovalueStr': lowIsovalueStr,
                'upperIsoIndex': upperIsoIndex,
                'upperIsovalueStr': upperIsovalueStr
            }

        for i in range(len(dots)):
            curDot = dots[i]
            cellColumnIndex = math.floor((curDot[0] - self.m_xMin) / step)
            cellRowIndex = math.floor((self.m_yMax - curDot[1]) / step)
            # ? 不知道用处
            # overlap = self.m_OC_liOverlap[cellRowIndex * 100 + cellRowIndex]
            sihoutte = None
            closePos = []
            if(len(liSihoutteIndex) > i):
                sihoutte = liSihoutteIndex[i]
            else:
                sihoutte = 1
            
            sensitivity = None
            if(len(liSensitivity) > i):
                sensitivity = liSensitivity[i]
            else:
                sensitivity = 0
            isoBag = mapDotIndexIsoBag[i]
            lowIsoIndex = isoBag['lowIsoindex']
            lowIsovalueStr = isoBag['lowIsoValuestr']
            upperIsovalueStr = isoBag['upperIsoindex']
            upperIsoIndex = isoBag['upperIsoValuestr']

            dotType = 'none'
            if lowIsoIndex == minLowIsoIndex:
                dotType = 'boundary'
            else:
                dotType = i


            # get the interpolate isocontour
            # get the closest isocontour
            closeContour = None
            closePointIndex = -1
            liCandiateContour = []
            for p in range(len(mapIsovalueCanvasContour[lowIsovalueStr])):
                liCandiateContour.append(mapIsovalueCanvasContour[lowIsovalueStr[p]])
            if(upperIsovalueStr in mapIsovalueCanvasContour.keys()):
                for p in range(len(mapIsovalueCanvasContour[upperIsovalueStr])):
                    liCandiateContour.append(mapIsovalueCanvasContour[upperIsovalueStr][p])
            mapInterContours = mapIsovalueInterContours[lowIsovalueStr]
            for keys_temp in mapInterContours:
                liCandiateContour.append(mapInterContours[keys_temp])
            
            centroidPos = mapIsovalueStrCentroids[lowIsovalueStr][0]
            minDistance = 1e6

            if lowIsoIndex < 3:
                closeContourIndex = -1
                for j in range(len(liCandiateContour)):
                    curIntersection = self.getRadialIntersection(centroidPos, curDot, liCandiateContour[j])
                    curIntersectPos = curIntersection['pos']
                    distance_temp = (curIntersectPos[0] - curDot[0]) * (curIntersectPos[0] - curDot[0]) + (curIntersectPos[1] - curDot[1]) * (curIntersectPos[1] - curDot[1])
                    if(minDistance > distance_temp):
                        closeContour = liCandiateContour[j]
                        closePointIndex = curIntersection['index']
                        closePos = curIntersectPos
                        closeContourIndex = j
                        minDistance = distance_temp
            else:
                for j in range(len(liCandiateContour)):
                    contour_temp = liCandiateContour[j]
                    for p in range(len(contour_temp)):
                        dot_temp = contour_temp[p]
                        distance_temp = self.geoInstance.getDis(dot_temp, curDot)
                        if minDistance > distance_temp:
                            closeContour = contour_temp
                            closePointIndex = p
                            closePos = dot_temp
                            closeContourIndex = j
                            minDistance = distance_temp

            tempContourKey = str(lowIsoIndex) + '_' + str(closeContourIndex)
            if tempContourKey not in mapIsovalueIndexContour.keys():
                mapIsovalueIndexContour[tempContourKey] = closeContour
            
            # if(dotType == 'boundary'){
            #     this.m_drawInterContour['dots'] = [centroidPos];
            # }
        
            curve = []
            disToCentroid = self.geoInstance.getDis(curDot, centroid)

            if(self.m_OC_PointDisToCentroid_min > disToCentroid):		
                self.m_OC_PointDisToCentroid_min = disToCentroid
            if(self.m_OC_PointDisToCentroid_max < disToCentroid):
                self.m_OC_PointDisToCentroid_max = disToCentroid
            
            if(pointToCentroid_min > disToCentroid):		
                pointToCentroid_min = disToCentroid
            if(pointToCentroid_max < disToCentroid):
                pointToCentroid_max = disToCentroid;

            curveBag = {
                'dotType': dotType,
                'dots': [],
                'longdots': [],
                'sortIsoValueIndex': lowIsoIndex,
                'centroid': centroid,
                'sihoutte': sihoutte,
                'sensitivity': sensitivity,
                # 上面注释了所以这儿也注释了
                #? 'overlap': overlap,
                'distanceToCentroid': disToCentroid,
                'intersection': closePos,
                'indersectionIndex': closePointIndex,
            }

            curveLength = None

            # if g_sensityvityRender == False:
            curveLength = self.getLengthBySI(sihoutte)
            # else:
                # curveLength = self.getLengthBySI(sensitivity)
            curveLength = self.getLengthSpecialCase(curveLength, sihoutte)

            if(curveLength > maxLength):
                maxLength = curveLength
            if(curveLength < minLength):
                minLength = curveLength
            
            curveBag['strokeLength'] = curveLength
            leftLength = curveLength/2
            rightLength = curveLength/2;

            diff = self.m_diff
            if closeContour is not None:
                if curveBag['dotType'] is not None:
                    curveBag['baseDot'] = closePos
                    curBaseDot = curveBag['baseDot']
                    diffVector = [0, 0]
                    if diff:
                        diffVector = [curDot[0] - curBaseDot[0], curDot[1] - curBaseDot[1]]
                    
                    # ? 
                    self.m_drawInterContour['dots1'] = []
                    self.m_drawInterContour['dots2'] = []
                    liLeftDot = []
                    curveBag['dots'] = []

                    if leftLength != 0:
                        # ? 
                        self.m_drawInterContour['reddots'] = [closePos]
                        self.m_drawInterContour['blackdots'] = [curDot]

                        # ?left
                        leftPos = closePos
                        tobeAddPointIndex = closePointIndex
                        tobeAddPos = closeContour[tobeAddPointIndex]
                        tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)
                        while tobeAddLength <= leftLength:
                            self.m_drawInterContour['dots1'].append(tobeAddPos)
                            liLeftDot.append(tobeAddPos)
                            tobeAddPointIndex -= 1
                            if tobeAddPointIndex < 0:
                                tobeAddPointIndex = len(closeContour) - 1
                            leftLength -= tobeAddPointIndex
                            leftPos = tobeAddPos
                            tobeAddPos = closeContour[tobeAddPointIndex]
                            tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)

                        if leftLength < tobeAddLength:
                            interPos = self.geoInstance.getPosinLine(leftPos, tobeAddPos, leftLength)
                            self.m_drawInterContour['dot1'].append(interPos)
                            liLeftDot.append(interPos)
                        for temp in range(len(liLeftDot)-1, -1, -1):
                            curveBag['dots'].append([liLeftDot[temp][0] + diffVector[0], liLeftDot[temp][1] + diffVector[1]])

                    if diff:
                        curveBag['dots'].append(curDot)
                    else:
                        curveBag['dots'].append(closePos)

                    # right
                    if rightLength != 0:
                        leftPos = closePos
                        tobeAddPointIndex = closePointIndex + 1
                        if tobeAddPointIndex >= len(closeContour):
                            tobeAddPointIndex = 0
                        tobeAddPos = closeContour[tobeAddPointIndex]
                        # if tobeAddPos is None:
                        tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)
                        while tobeAddLength <= rightLength:
                            self.m_drawInterContour['dots2'].append(tobeAddPos)
                            curveBag['dots'].append([tobeAddPos[0] + diffVector[0], tobeAddPos[1] + diffVector[1]])
                            tobeAddPointIndex += 1
                            if tobeAddPointIndex >= len(closeContour):
                                tobeAddPointIndex = 0
                            rightLength -= tobeAddPointIndex
                            # ? spcanvas.js中第3172行是leftPos leftPos = tobeAddPos
                            rightPos = tobeAddPos
                            tobeAddPos = closeContour[tobeAddPointIndex]
                            # ? spcanvas.js 第 3174行也是leftPos
                            tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)

                        if rightLength < tobeAddLength:
                            # ? spcanvas.js 3177行也是leftPos
                            interPos = self.geoInstance.getPosinLine(leftPos, tobeAddPos, rightLength)
                            self.m_drawInterContour['dot2'].append(interPos)
                            liLeftDot.append(interPos)
                            curveBag['dots'].append([liLeftDot[0] + diffVector[0], liLeftDot[1] + diffVector[1]])
                else:
                    curveBag['dots']  = []   
            # if len(curveBag['dots']) == 0
            mapIndexStrokeBag[i] = curveBag
        
        mapIndexCurve = self.adjustStrokesofClass(mapIndexStrokeBag)

        mapIsovalueIndex = {}
        for curKey in mapIsovalueIndexContour:
            contour = mapIsovalueIndexContour[curKey]
            curKeySplit = curKey.split('_')
            isovalue = curKeySplit[0]
            index = curKeySplit[1]
            if isovalue not in mapIsovalueIndex.keys():
                mapIsovalueIndex[isovalue] = index
            elif int(mapIsovalueIndex[isovalue] < index):
                mapIsovalueIndex[isovalue] = index
        liRelatedContour = []
        for curKey in mapIsovalueIndex:
            key_temp = curKey + '_' + mapIsovalueIndex[curKey]
            liRelatedContour.append(mapIsovalueIndexContour[key_temp])
        return [mapIndexCurve, mapIndexStrokeBag, liRelatedContour, [pointToCentroid_min, pointToCentroid_max], [maxLength, minLength]]

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
                for j in range(len(clusterInfo)):
                    if (i == j):
                        continue
                    curClusterId2 = clusterInfo[j]['classId']
                    curLiDots2 = clusterInfo[j]['dots']
                    tempAvgB = 0
                    for k in range(len(curLiDots2)):
                        if (curClusterId1 > curClusterId2):
                            if((str(curClusterId2) + '_' + str(k) + '-' + str(curClusterId1) + '_' + str(p)) in self.m_mapDisMatrix == False):
                                tempAvgB += 10
                            else:
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId2) + '_' + str(k) + '-' + str(curClusterId1) + '_' + str(p)]
                        else:
                            if((str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(k)) in self.m_mapDisMatrix == False):
                                tempAvgB += 10
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(k)]
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
            # outIsoValue = liSortedIsoValueStr[1]
            outIsoValue = liSortedIsoValueStr[0]
            outContour = mapContours[outIsoValue][0]

            # 根据公共轮廓插值，并根据中心点与该点连线与contour的交集找到在contour上离该点最近的点
            mapNewIndexContours = self.interpolateContourSelf(outContour, 20)

            mapNewCanvasContours = {}
            mapNewIsoValueInnerContours = {}
            mapNewCanvasContours[outIsoValue] = [outContour]
            mapNewIsoValueInnerContours[outIsoValue] = mapNewIndexContours

            result = self.preLocate(curDots, liSihoutteIndex, liSensitivity, liKDE, 
                mapNewCanvasContours, mapNewIsoValueInnerContours, [outIsoValue])

    def startDrawWinglets(self, dotsData, clusterInfo):
        liClusterInfo = clusterInfo['clusters']
        canvasRange = clusterInfo['canvasRange']
        self.m_xMin = canvasRange[0]
        self.m_xMax = canvasRange[1]
        self.m_yMin = canvasRange[2]
        self.m_yMax = canvasRange[3]

        self.computeDisMatrix(dotsData)
        self.computeSilhouette(liClusterInfo)

        self.computeDotStrokes(liClusterInfo)
        # self.computeColorMap(liClusterInfo)





