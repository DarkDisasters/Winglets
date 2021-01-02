import math;
from .geoOperation import getGeoInfo;
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
    m_mapClassIdMaxMinLength = {}
    m_mapClassIdDotIndexStroke = {}
    m_mapClassIdDotIndexStrokeBag = {}
    m_WC_ClassIDPointDis_minmax = {}
    m_test_mainContour = {}

    m_xMin = 0
    m_xMax = 0
    m_yMin = 0
    m_yMax = 0
    m_OC_PointDisToCentroid_min = 1e6
    m_OC_PointDisToCentroid_max = -1e6
    m_diff = True

    geoInstance = getGeoInfo()

    def dot2Canvas(self, dot, scale=8):
        
        return [scale * dot[0], scale * dot]
    
    def convertContourToCanvas(self, mapIsovalueContours):
        mapIsovalueCanvasContours = {}
        for Isovalue in mapIsovalueContours:
            contours = mapIsovalueContours[Isovalue]
            for i in range(len(contours)):
                contour = contours[i]
                canvasContour = []
                for p in range(len(contour)):
                    pos = contour[p]
                    canvasContour.append(self.dot2Canvas([pos[1], 100 - pos[0]]))
                    if Isovalue not in mapIsovalueCanvasContours.keys():
                        mapIsovalueCanvasContours[Isovalue] = [canvasContour]
                    else:
                        mapIsovalueCanvasContours[Isovalue].append(canvasContour)
        return mapIsovalueCanvasContours

    # 不知道有啥用
    def sortIsovalue(self, mapIsovalueContour):
        liSortedIsovalueStr = []
        liIsovalueStr = list(mapIsovalueContour.keys())
        liNewIsovalue = []

        for i in range(len(liIsovalueStr)):
            # liNewIsovalue.append(int(liIsovalueStr[i]))
            liNewIsovalue.append(float(liIsovalueStr[i]))
        liNewIsovalue.sort()

        for i in range(len(liNewIsovalue)):
            curIsovalueNum = liNewIsovalue[i]
            for j in range(len(liIsovalueStr)):
                # IsovalueTmp = int(liIsovalueStr[j])
                IsovalueTmp = float(liIsovalueStr[j])
                if(abs(curIsovalueNum - IsovalueTmp) < 1e-6):
                    liSortedIsovalueStr.append(liIsovalueStr[j])
        return liSortedIsovalueStr

    def getRadialIntersection(self, pos1, pos2, contour):
        centroidPos = Point(pos1[0], pos1[1])
        # centroidPos = Point(1500 * pos1[0] - 1500 * pos2[0], 1500 * pos1[1] - 1500 * pos2[1])
        dataPos = Point(3000 * pos2[0] - 3000 * pos1[0] + pos1[0], 3000 * pos2[1] - 3000 * pos1[1] + pos1[1])
        # dataPos = Point(1500 * pos2[0], 1500 * pos2[1])
        # dataPos = Point(pos2[0] - pos1[0], pos2[1] - pos1[1])
        centroidAlongLinePath = LineString([centroidPos, dataPos])

        contourPathPoints = []
        for i in range(len(contour)):
            contourPathPoints.append(Point(contour[i][0], contour[i][1]))
        # 因为shapely没有添加的api，所以将点放在数组里使用Polygon一次性生成polygon
        contourPath = Polygon(contourPathPoints)

        # 通过shapely的intersection获取到LineString和Polygon的交集，应该是一条lineString，可以用coords来获取交集的点
        # 如果交集为一个线段，一个点为交点，一个点为线段中的一个点，一般是第一个元素
        # liIntersectionsCoords = list(contourPath.intersection(centroidAlongLinePath).coords)
        # print('test', centroidAlongLinePath.intersection(contourPath))
        liIntersections = centroidAlongLinePath.intersection(contourPath)
        liIntersectionsCoords = []
        if (liIntersections.type == 'MultiLineString'):
            print('multiLineString')
            listLiIntersections = list(liIntersections)
            for i in range(len(listLiIntersections)):
                if i == 0:
                    curIntersectionLineStringCoords = list(listLiIntersections[i].coords)
                    print('curDot1', centroidPos)
                    print('pos2', pos2)
                    print('curDot2', dataPos)
                    print('curIntersectionLineStringCoords', curIntersectionLineStringCoords)
                    # liIntersectionsCoords.append(curIntersectionLineStringCoords[0])
                    liIntersectionsCoords.append(curIntersectionLineStringCoords[1])
                # liIntersectionsCoords.append(list(listLiIntersections[i].coords))
            # liIntersectionsCoords= list(listLiIntersections[0].coords)
        else:
            # liIntersectionsCoords = list(centroidAlongLinePath.intersection(contourPath).coords)
            liIntersectionsCoords = list(centroidAlongLinePath.intersection(contourPath).coords)
            liIntersectionsCoords = [liIntersectionsCoords[1]]
            # print('liIntersectionsCoords', liIntersectionsCoords)
            # print('liIntersectionsCoords[1]', liIntersectionsCoords[1])

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
    	
        minDistanceOnContour = 1e6
        minIndexOnContour = -1
        curIntersectionPos = [liIntersectionsCoords[minIndex][0], liIntersectionsCoords[minIndex][1]]
        for i in range(len(contour)):
            dis_temp_onContour = math.sqrt(math.pow(curIntersectionPos[0] - contour[i][0], 2) + math.pow(curIntersectionPos[1] - contour[i][1], 2))
            if dis_temp_onContour < minDistanceOnContour:
                minIndexOnContour = i
                minDistanceOnContour = dis_temp_onContour

        # if minDistanceOnContour < 5:
        #     return {
        #         # 'pos': [liIntersectionsCoords[minIndex][0], liIntersectionsCoords[minIndex][1]],
        #         'pos': curIntersectionPos,
        #         #? intersections[minIndex].index
        #         'index': minIndexOnContour
        #     }
        # else:
        #     print('curDistance > 1', minDistanceOnContour)
        # if minDistanceOnContour > 3:
        #     print('curDistance > 1', minDistanceOnContour)

        # contour.insert(minIndexOnContour, curIntersectionPos)

        return {
            # 'pos': [liIntersectionsCoords[minIndex][0], liIntersectionsCoords[minIndex][1]],
            'pos': curIntersectionPos,
            #? intersections[minIndex].index
            'index': minIndexOnContour
            }
        



    def interpolateContourSelf(self, contour, contourNum):
        mapIndexContour = {}
        liDeformVector = []
        sampleNum = 120
        # print('contour', contour)
        # 算出当前contour的centroid，此时的contour为前几步找到的当前class中的应该保留的外层公共contour
        centroidPos = self.geoInstance.getCentroid(contour)
        # 希望的是将当前公共contour分成120份，对每一份求交点来对每一份进行插值 ？分成120份的意义
        for i in range(sampleNum):
            # 这个arc就可以在下面帮助生成中心点在当前i份中(120份中的第i份)发出的射线
            arc = (i * 2 * math.pi) / sampleNum
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
        # ? 本来是15, 但是太短了
        curveLength = s + curSI * 18
        if curveLength < s:
            curveLength = s
        return curveLength
    
    def adjustStrokesofClass(self, mapIndexStrokeBag):
        mapIndexCurve = {}
        # finer the curve and adapt to contourIndex
        liDotIndex = list(mapIndexStrokeBag.keys())
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
                'originDot': curveBag['originDot'],
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
        liIsovalue = list(mapIsovalueCanvasContour.keys())  #?获得的应该是最外层contour的Isovalue，因为mapIsovalueCanvasContour只保留了outContour

        mapIsovalueIndexContour = {}
        mapIsovalueStrCentroids = {}

        # compute the centroid of contours，计算的是 每个Isovalue下每个contour的centroid ？但是mapIsovalueCanvasContour里面放的是外层的公共contour
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

        step = (self.m_xMax - self.m_xMin) / 100    # step = 8
        mapDotIndexIsoBag = {}
        minLength = 1e6
        maxLength = -1e6

        # get the closest minIsovalue_str and minContourIndex
        minLowIsoIndex = 1e6
        for i in range(len(dots)):
            curDot = dots[i]
            # 确定当前点应该在800x800的哪个格子里（以8为单位）
            cellColumnIndex = math.floor((curDot[0] - self.m_xMin) / step)
            cellRowIndex = math.floor((self.m_yMax - curDot[1]) / step)
            density = liKDE[cellRowIndex * 100 + cellColumnIndex]

            # get the two boundary
            lowIsovalueStr = upperIsovalueStr = None
            lowIsoIndex = upperIsoIndex = -1
            #？liSortedIsovalueStr里只有[outIsovalue]，这个循环会跳过
            for j in range(len(liSortedIsovalueStr) - 1):
                Isovalue1 = float(liSortedIsovalueStr[j])
                Isovalue2 = float(liSortedIsovalueStr[j + 1])
                if(Isovalue1 <= density and Isovalue2 >= density):
                    lowIsovalueStr = liSortedIsovalueStr[j]
                    upperIsovalueStr = liSortedIsovalueStr[j+1]
                    lowIsoIndex = j
                    upperIsoIndex = j+1
                    if(lowIsoIndex < minLowIsoIndex):
                        minLowIsoIndex = lowIsoIndex

            #? 得清楚这几个是干嘛的, 是为了记录离点最近的isovalue和isovalue对应的contour的index嘛 因为上面的循环不能运行，lowIsoIndex = 0，lowIsovalueStr为最外层contour的Isovalue，upperIsoIndex=1，minLowIsoIndex = 0
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

        # 为每个点添加winglets
        # 不知道上面的循环时干嘛的, 都是对 dots遍历, 上面几乎没做什么, 只是将lowIsoIndex等值存入, 且都是初始化时的值
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
            lowIsoIndex = isoBag['lowIsoIndex']
            lowIsovalueStr = isoBag['lowIsovalueStr']
            upperIsovalueStr = isoBag['upperIsoIndex']
            upperIsoIndex = isoBag['upperIsovalueStr']

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
                liCandiateContour.append(mapIsovalueCanvasContour[lowIsovalueStr][p])
            #？不懂这个地方的用处，
            if(upperIsovalueStr in mapIsovalueCanvasContour.keys()):
                for p in range(len(mapIsovalueCanvasContour[upperIsovalueStr])):
                    liCandiateContour.append(mapIsovalueCanvasContour[upperIsovalueStr][p])
            # 将插值得到的contour中最外层Isovalue值得contour赋给了mapInterContour，并把个Isovalue下得contour添加在了liCandiateContour，？感觉不对
            mapInterContours = mapIsovalueInterContours[lowIsovalueStr]
            for keys_temp in mapInterContours:
                liCandiateContour.append(mapInterContours[keys_temp])
            
            # print('liCandiateContour len', len(liCandiateContour))
            # if len(liCandiateContour) != 1:
            #     print('liCandiateContour', liCandiateContour)
            
            centroidPos = mapIsovalueStrCentroids[lowIsovalueStr][0]
            minDistance = 1e6

            if lowIsoIndex < 3:
                closeContourIndex = -1
                for j in range(len(liCandiateContour)):
                    curIntersection = self.getRadialIntersection(centroidPos, curDot, liCandiateContour[j])
                    curIntersectPos = curIntersection['pos']
                    distance_temp = (curIntersectPos[0] - curDot[0]) * (curIntersectPos[0] - curDot[0]) + (curIntersectPos[1] - curDot[1]) * (curIntersectPos[1] - curDot[1])
                    if(minDistance > distance_temp):
                        # 只是将contour中值赋值给了closeContour
                        closeContour = liCandiateContour[j][:]
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
            
            # 将 closePos与就是交点插入closeContour里, 改变closePointIndex, 并将随后的index整体加一
            tempLeftIndex = closePointIndex - 1 
            tempRightIndex = closePointIndex + 1 
            if closePointIndex == len(closeContour)-1:
                tempRightIndex = 0
            if closePointIndex == 0:
                tempLeftIndex = len(closeContour)-1
            leftPosToClosePosDis = self.geoInstance.getDis(closeContour[tempLeftIndex], closePos)
            rightPosToClosePosDis = self.geoInstance.getDis(closeContour[tempRightIndex], closePos)
            if leftPosToClosePosDis < rightPosToClosePosDis:
                closeContour.insert(closePointIndex, closePos)
            else:
                closeContour.insert(tempRightIndex, closePos)
                closePointIndex = tempRightIndex

            # ? 这个应该时临时存储每个点 最近的contour
            tempContourKey = str(lowIsoIndex) + '_' + str(closeContourIndex)
            if tempContourKey not in mapIsovalueIndexContour.keys():
                mapIsovalueIndexContour[tempContourKey] = closeContour
            
            # if(dotType == 'boundary'){
            #     this.m_drawInterContour['dots'] = [centroidPos];
            # }
        
            curve = []
            # ？centroid的定义在哪
            disToCentroid = self.geoInstance.getDis(curDot, centroid)

            if(self.m_OC_PointDisToCentroid_min > disToCentroid):		
                self.m_OC_PointDisToCentroid_min = disToCentroid
            if(self.m_OC_PointDisToCentroid_max < disToCentroid):
                self.m_OC_PointDisToCentroid_max = disToCentroid
            
            if(pointToCentroid_min > disToCentroid):		
                pointToCentroid_min = disToCentroid
            if(pointToCentroid_max < disToCentroid):
                pointToCentroid_max = disToCentroid;

            # 这个是循环每个点都会定义的curveBag，为该点接下来画curve做准备，最重要的是后三个属性
            # distanceToCentroid存放当前点到？上面的有问题 311行
            # intersection和intersectionIndex存放离当前点最近的位于contour上的点坐标和closePointIndex = curIntersection['index']/closePointIndex = p
            curveBag = {
                'dotType': dotType,
                'dots': [],
                'longdots': [],
                'originDot': curDot,
                'sortIsovalueIndex': lowIsoIndex,
                'centroid': centroid,
                'sihoutte': sihoutte,
                'sensitivity': sensitivity,
                # 上面注释了所以这儿也注释了
                #? 'overlap': overlap,
                'distanceToCentroid': disToCentroid,
                'intersection': closePos,
                'intersectionIndex': closePointIndex,
            }

            curveLength = None

            # if g_sensityvityRender == False:
            curveLength = self.getLengthBySI(sihoutte)
            # else:
                # curveLength = self.getLengthBySI(sensitivity)
            curveLength = self.getLengthSpecialCase(curveLength, sihoutte)
            # 
            # curveLength = 20

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
                    # 将最近的点放在当前点的curveBag的baseDot里
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

                        # left 左半部分的winglets, tobeAddLength初始应该是0, 所以有个while判断, 将当前的contour上的点压入drawInterContour的dots1里面,也压入liLeftDot里
                        # 当这个length大于leftLength也就是满足了我们想要的winglets左半部分的长度后就结束循环
                        leftPos = closePos
                        tobeAddPointIndex = closePointIndex
                        tobeAddPos = closeContour[tobeAddPointIndex]
                        tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)
                        while tobeAddLength <= leftLength:
                            self.m_drawInterContour['dots1'].append(tobeAddPos)
                            liLeftDot.append(tobeAddPos)
                            tobeAddPointIndex -= 1
                            if tobeAddPointIndex < 0:
                                # ? name = 4的时候 tobeAddPointIndex = len(closeContour) - 1 和 tobeAddPointIndex = 0时数据点是一样的
                                # tobeAddPointIndex = len(closeContour) - 1
                                print('left: pointIndex < 0')
                                tobeAddPointIndex = len(closeContour) - 1
                                # print('tobeAddPointIndex < 0',tobeAddPointIndex)
                                # print('tobeAddPointIndex[0]',closeContour[0])
                                # print('tobeAddPointIndex[len(closeContour) - 1]',closeContour[len(closeContour) - 1])
                            leftLength -= tobeAddLength
                            leftPos = tobeAddPos
                            tobeAddPos = closeContour[tobeAddPointIndex]
                            tobeAddLength = self.geoInstance.getDis(leftPos, tobeAddPos)

                        if leftLength < tobeAddLength:
                            # print('leftPos', leftPos)
                            # print('tobeAddPointIndex',tobeAddPointIndex)
                            interPos = self.geoInstance.getPosinLine(leftPos, tobeAddPos, leftLength)
                            self.m_drawInterContour['dots1'].append(interPos)
                            liLeftDot.append(interPos)
                        for temp in range(len(liLeftDot)-1, -1, -1):
                            curveBag['dots'].append([liLeftDot[temp][0] + diffVector[0], liLeftDot[temp][1] + diffVector[1]])

                    if diff:
                        curveBag['dots'].append(curDot)
                    else:
                        curveBag['dots'].append(closePos)

                    # right
                    # if rightLength != 0:
                    #     rightPos = closePos
                    #     tobeAddPointIndex = closePointIndex + 1
                    #     if tobeAddPointIndex >= len(closeContour):
                    #         tobeAddPointIndex = 0
                    #     tobeAddPos = closeContour[tobeAddPointIndex]
                    #     # if tobeAddPos is None:
                    #     tobeAddLength = self.geoInstance.getDis(rightPos, tobeAddPos)
                    #     while tobeAddLength <= rightLength:
                    #         self.m_drawInterContour['dots2'].append(tobeAddPos)
                    #         curveBag['dots'].append([tobeAddPos[0] + diffVector[0], tobeAddPos[1] + diffVector[1]])
                    #         tobeAddPointIndex += 1
                    #         if tobeAddPointIndex >= len(closeContour):
                    #             tobeAddPointIndex = 0
                    #         rightLength -= tobeAddLength
                    #         # ? spcanvas.js中第3172行是leftPos leftPos = tobeAddPos
                    #         rightPos = tobeAddPos
                    #         tobeAddPos = closeContour[tobeAddPointIndex]
                    #         # ? spcanvas.js 第 3174行也是leftPos
                    #         tobeAddLength = self.geoInstance.getDis(rightPos, tobeAddPos)

                    #     if rightLength < tobeAddLength:
                    #         # ? spcanvas.js 3177行也是leftPos
                    #         interPos = self.geoInstance.getPosinLine(rightPos, tobeAddPos, rightLength)
                    #         self.m_drawInterContour['dots2'].append(interPos)
                    #         curveBag['dots'].append([interPos[0] + diffVector[0], interPos[1] + diffVector[1]])
                    if rightLength != 0:
                        rightPos = closePos
                        tobeAddPointIndex = closePointIndex + 1
                        if tobeAddPointIndex >= len(closeContour):
                            print('cccc')
                            tobeAddPointIndex = 0
                        tobeAddPos = closeContour[tobeAddPointIndex]
                        # if tobeAddPos is None:
                        tobeAddLength = self.geoInstance.getDis(rightPos, tobeAddPos)
                        while tobeAddLength <= rightLength:
                            self.m_drawInterContour['dots2'].append(tobeAddPos)
                            curveBag['dots'].append([tobeAddPos[0] + diffVector[0], tobeAddPos[1] + diffVector[1]])
                            tobeAddPointIndex += 1
                            if tobeAddPointIndex >= len(closeContour):
                                print('right: pointIndex >= len(closeContour)')
                                tobeAddPointIndex = 0
                            rightLength -= tobeAddLength
                            # ? spcanvas.js中第3172行是leftPos leftPos = tobeAddPos
                            rightPos = tobeAddPos
                            tobeAddPos = closeContour[tobeAddPointIndex]
                            # ? spcanvas.js 第 3174行也是leftPos
                            tobeAddLength = self.geoInstance.getDis(rightPos, tobeAddPos)

                        if rightLength < tobeAddLength:
                            # ? spcanvas.js 3177行也是leftPos
                            interPos = self.geoInstance.getPosinLine(rightPos, tobeAddPos, rightLength)
                            self.m_drawInterContour['dots2'].append(interPos)
                            curveBag['dots'].append([interPos[0] + diffVector[0], interPos[1] + diffVector[1]])
                else:
                    curveBag['dots']  = []   
            
            mapIndexStrokeBag[i] = curveBag
        
        mapIndexCurve = self.adjustStrokesofClass(mapIndexStrokeBag)

        mapIsovalueIndex = {}
        for curKey in mapIsovalueIndexContour:
            contour = mapIsovalueIndexContour[curKey]
            curKeySplit = curKey.split('_')
            Isovalue = curKeySplit[0]
            index = curKeySplit[1]
            if Isovalue not in mapIsovalueIndex.keys():
                mapIsovalueIndex[Isovalue] = index
            elif int(mapIsovalueIndex[Isovalue] < index):
                mapIsovalueIndex[Isovalue] = index
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
                        # curDistance = distanceOpeInstance.getDifClassDotDistance([curDot1['x'], curDot1['y']], [curDot2['x'], curDot2['y']])
                        curDistance = self.geoInstance.getDis([curDot1['x'], curDot1['y']], [curDot2['x'], curDot2['y']])
                        self.m_mapDisMatrix[str(curCluster1) + '_' + str(p) + '-' + str(curCluster2) + '_' + str(q)] = curDistance
                        self.m_mapDisMatrix[str(curCluster2) + '_' + str(q) + '-' + str(curCluster1) + '_' + str(p)] = curDistance
    
    def computeSilhouette(self, clusterInfo):
        # 在全局定义了
        # m_mapClassIDDotIndexSihouttle = {}  # 以class为key存放当前类的所有点的关于sihoutte的一个比值，(当前值-最小silhoutte值) / (最大silhoutte值-最小silhoutte值)
        # m_mapClassIDMaxMinSI = {}   # 以class为key存放当前类silhoutte的最大最小值，数组形式

        disMatrix = self.m_mapDisMatrix
        g_Max = 1e-6
        g_Min = 1e6

        for i in range(len(clusterInfo)):
            curClusterId1 = clusterInfo[i]['classId']

            liNormalSIIndex = []    
            liSilhoutteIndex = []   
            silhoutte_min = 1e6
            silhoutte_max = 1e-6

            curLiDots1 = clusterInfo[i]['dots']
            
            #计算当前class中每个点与该类中其他点的距离求均值放于avgA中，
            #计算当前class中每个点与其他类中所有点的距离求均值，将最小的?的均值放于avgB中
            # 根据上面的avgA和avgB求silhouette
            for p in range(len(curLiDots1)):
                avgA = 0
                #avgA为和同一类点求距离
                for q in range(len(curLiDots1)):
                    # if self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)] == 0:
                    #     print('hhhhhhhh')
                    if((str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)) in self.m_mapDisMatrix):
                        avgA += self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId1) + '_' + str(q)]
                    else:
                        print('avgA test None')
                        avgA += 5
                avgA /= len(curLiDots1)
                sihoutte = None
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
                                print('avgB test None')
                                tempAvgB += 10
                            else:
                                if self.m_mapDisMatrix[str(curClusterId2) + '_' + str(k) + '-' + str(curClusterId1) + '_' + str(p)] == 0:
                                    print('hhhhh2')
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId2) + '_' + str(k) + '-' + str(curClusterId1) + '_' + str(p)]
                        else:
                            if((str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(k)) in self.m_mapDisMatrix == False):
                                print('avgB test None')
                                tempAvgB += 10
                            else:
                                if self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(k)] == 0:
                                    print('hhhhh3')
                                tempAvgB += self.m_mapDisMatrix[str(curClusterId1) + '_' + str(p) + '-' + str(curClusterId2) + '_' + str(k)]
                    # ? 只用计算该店与各个类分别的距离再选择其中最小的？
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
            
            # liSihoutteIndex 当前class的各个点的silhoutte
            # liNormalSIIndex 存放的是当前类的各个点的关于sihoutte的一个比值，(当前值-最小silhoutte值) / (最大silhoutte值-最小silhoutte值)
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
            mainIsovalue = clusterInfo[i]['mainIsovalue']
            self.m_test_mainContour[curClusterId] = mainContour

            mapMainIsoContour = {}
            mapDotIndexDeepIsoIndex = {}

            mapIsovalueCanvasContours = self.convertContourToCanvas(mapContours)
            #不知道排序的作用
            liSortedIsovalueStr = self.sortIsovalue(mapContours)
            clusterInfo[i]['sortedIsovalue'] = liSortedIsovalueStr

            outContour = []
            # spcanvas.js第1575行有几个if判断，不知道选哪个
            outIsovalue = mainIsovalue
            outContour = mainContour

            # 根据公共轮廓插值，并根据中心点与该点连线与contour的交集找到在contour上离该点最近的点
            # ? 如果 只用最外层的contour作为标准，那插值的作用
            mapNewIndexContours = self.interpolateContourSelf(outContour, 20)

            mapNewCanvasContours = {}   #存放的是最外层的最开始生成的公共contour
            mapNewIsovalueInnerContours = {}    #存放的是interpolateContourSelf生成的所有插值生成的contour
            mapNewCanvasContours[outIsovalue] = [outContour]
            mapNewIsovalueInnerContours[outIsovalue] = mapNewIndexContours

            # result = self.preLocate(curDots, liSihoutteIndex, liSensitivity, liKDE, 
            #     mapNewCanvasContours, mapNewIsovalueInnerContours, [outIsovalue])
            result = self.preLocate(curDots, liSihoutteIndex, liSensitivity, liKDE, 
                mapNewCanvasContours, mapNewIsovalueInnerContours, [outIsovalue])
            
            self.m_mapClassIdMaxMinLength[curClusterId] = [result[4][0], result[4][1]]
            clusterInfo[i]['canvascontours'] = []

            for iso in mapIsovalueCanvasContours:
                for temp in range(len(mapIsovalueCanvasContours[iso])):
                    clusterInfo[i]['canvascontours'].append(mapIsovalueCanvasContours[iso][temp])

            clusterInfo[i]['interpolatecontours'] = []
            for index_temp in mapNewIsovalueInnerContours[outIsovalue]:
                clusterInfo[i]['interpolatecontours'].append(mapNewIsovalueInnerContours[outIsovalue][index_temp])
            clusterInfo[i]['mainContour'] = mainContour

            self.m_mapClassIdDotIndexStroke[curClusterId] = result[0]
            self.m_mapClassIdDotIndexStrokeBag[curClusterId] = result[1]
            self.m_WC_ClassIDPointDis_minmax[curClusterId] = result[3]
        return clusterInfo

    def startDrawWinglets(self, dotsData, clusterInfo):
        liClusterInfo = clusterInfo['clusters']
        canvasRange = clusterInfo['canvasRange']
        self.m_xMin = canvasRange[0]
        self.m_xMax = canvasRange[1]
        self.m_yMin = canvasRange[2]
        self.m_yMax = canvasRange[3]

        self.computeDisMatrix(dotsData)
        self.computeSilhouette(liClusterInfo)

        curClusterInfo = self.computeDotStrokes(liClusterInfo)
        # print('self.m_mapClassIdDotIndexStroke', self.m_mapClassIdDotIndexStroke)
        # self.computeColorMap(liClusterInfo)
        return curClusterInfo, self.m_mapClassIdDotIndexStroke, self.m_test_mainContour





