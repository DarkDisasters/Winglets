import math;
import numpy as np;
from scipy import stats;
from skimage import measure;
from sklearn.cluster import KMeans

from .geoOperation import getGeoInfo;
from shapely.geometry import Point;
from shapely.geometry import Polygon;

import seaborn as sns
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

class Distance():
    def distanceCompute(self, dotInfo):
        sourceAndTarget = [];
        for i in range(len(dotInfo)):
            minDistance = float('inf');  #创建无穷大的值
            minTarget = 0
            for j in range(len(dotInfo)):
                if (j == i):
                    continue;
                else:
                    dx = abs(dotInfo[i]['x'] - dotInfo[j]['x']);
                    dy = abs(dotInfo[i]['y'] - dotInfo[j]['y']);
                    distance = math.sqrt(dx*dx + dy*dy);
                    if (distance < minDistance):
                        minDistance = distance
                        mintarget = j
            sourceAndTarget.append({
                'source': i,
                'target': j,
                'mindistance': minDistance
            })
        # print('sourceAndTarget', sourceAndTarget)
        return sourceAndTarget

class KDE():
    def listZip(self, m1, m2):
        list1 = list(m1);
        list2 = list(m2);
        return list(zip(list1, list2));

    def dot2Canvas(self, dotxy):
        #? 为啥是100 - 
        # ? 为啥 dotxy的 0 1 元素换位了
        dot = [dotxy[1], 100 - dotxy[0]]
        # dot = [dotxy[1], dotxy[0]]
        scale = 8
        return [scale * dot[0], scale * dot[1]] 

    def convert2Canvas(self, contour):
        newContour = []
        for dot in contour:
            scaleDot = self.dot2Canvas(dot)
            newContour.append(scaleDot)
        return newContour
    
    def kdeCore(self, m1, m2, xmin, xmax, ymin, ymax):
        # X, Y = np.mgrid[xmin:xmax:800j, ymin:ymax:800j]
        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()]);
        values = np.vstack([m1, m2]);
        kernel = stats.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        # drawKDEZX, drawKDEZY = np.reshape(kernel(positions).T, (2, 5000))
        # p1 = sns.kdeplot(drawKDEZX, drawKDEZY, cmap="Blues", shade=True, shade_lowest=True, )

        # plt.show()
        return np.rot90(Z)
        # return Z

    def getGlobalMaxDensityPoint(self, globalZ, curClassDots):
        mapIsovalueContours = {}
        isoPosNum = 10
        baseValue = 1e-9
        liIsovalue = []
        minDensity = globalZ.ravel().min()
        maxDensity = globalZ.ravel().max()
        proximityLowDensityPoints = []
        maxDensityPoints = []

        for i in range(isoPosNum-1, 0, -1):
            thresholdDensity = baseValue + i * (maxDensity - baseValue)/isoPosNum
            thresholdContours = measure.find_contours(globalZ, thresholdDensity, fully_connected='high')
            # thresholdContours = measure.find_contours(globalZ, thresholdDensity)
            thresholdPolygonArr = []
            # maxDensityPoints = []
            thresholdContainPointCount = 0

            for n, contour in enumerate(thresholdContours):
                contour = contour.tolist()
                if (len(contour) < 3):
                    continue
                # if (len(contour) < 2):
                #     contour.append([contour[0][0] + 1, contour[0][1] + 1])
                #     contour.append([contour[0][0] - 1, contour[0][1] - 1])
                # elif (len(contour) == 2):
                #     contour.insert(1, [(contour[0][0] + contour[1][0]) / 2, (contour[0][1] + contour[1][1]) / 2])
                # print('contour', contour)
                thresholdCanvasContour = self.convert2Canvas(contour)
                thresholdPolygon = Polygon(thresholdCanvasContour)
                thresholdPolygonArr.append(thresholdPolygon)
            for dot in curClassDots:
                    point = Point([dot['x'], dot['y']])
                    for index_temp in range(len(thresholdPolygonArr)):
                        polygon = thresholdPolygonArr[index_temp]
                        if(polygon.contains(point) == True):
                            thresholdContainPointCount += 1
                            maxDensityPoints.append([dot['x'], dot['y']])
                        else:
                            proximityLowDensityPoints.append([dot['x'], dot['y']])
            # print('count', thresholdContainPointCount)
            if thresholdContainPointCount < 30 and thresholdContainPointCount > 0:
                break
        print('count', thresholdContainPointCount)
        return maxDensityPoints, proximityLowDensityPoints

    def getContours(self, Z, dots):
        mapIsovalueContours = {}
        # isoPosNum = 10
        isoPosNum = 10
        baseValue = 1e-9
        liIsovalue = []
        minDensity = Z.ravel().min()
        maxDensity = Z.ravel().max()
        # ?不知道该不该加, 因为不加最低的isoValue为 1e-9, 比1e-1小,但是liIsovalue为 0.1, 1e-09 ,但是为什么加上后就可以 在计算kde是rotate90°并且画的contour没问题了
        # liIsovalue.append(1e-1)

        testDensity = baseValue + 9 * (maxDensity - baseValue)/isoPosNum
        testMaxContours = measure.find_contours(Z, testDensity, fully_connected='high')
        testMaxPolygonArr = []
        testMaxContainPointCount = 0
        maxDensityPoints = []
        for n, contour in enumerate(testMaxContours):
            contour = contour.tolist()
            if (len(contour) < 3):
                continue
            print('contour', contour)
            testMaxCanvasContour = self.convert2Canvas(contour)
            testMaxPolygon = Polygon(testMaxCanvasContour)
            testMaxPolygonArr.append(testMaxPolygon)
        for dot in dots:
                point = Point([dot['x'], dot['y']])
                for index_temp in range(len(testMaxPolygonArr)):
                    polygon = testMaxPolygonArr[index_temp]
                    if(polygon.contains(point) == True):
                        testMaxContainPointCount += 1
                        maxDensityPoints.append([dot['x'], dot['y']])
        # print('testMaxContainPointCount', testMaxContainPointCount)


        #根据设定的baseValue和isoPosNum按密度分段，将范围的每个值存入liIsoValue
        for i in range(isoPosNum):
            liIsovalue.append(baseValue + i * (maxDensity - baseValue)/isoPosNum)
        
        # print('liIsovalue', liIsovalue)
        
        #遍历设定的密度范围的分段值
        for i in range(len(liIsovalue)):
            #按照当前的 isoValue 生成contours
            curContours = measure.find_contours(Z, liIsovalue[i], fully_connected='high')

            curIsovalue = liIsovalue[i]
            #存放转化后的contours以及增加的信息
            curLiContours = []
            curLiPolygon = []

            #遍历按照当前isoValue生成的contour,因为同一个值可能生成两个互补重叠的contour，参考等高线
            for n, contour in enumerate(curContours):
                contour = contour.tolist();

                if (len(contour) == 0):
                    continue

                # 因数据点数量过少添加
                if (len(contour) < 3):
                    continue
                #将当前的contour以及设定count为0，用来统计当前isoValue生成的contour里有多少个点
                # curLiContours.append({
                #     'contour': contour,
                #     'count': 0
                # });
                # 缩放，此处我注释了
                curCanvasContour = self.convert2Canvas(contour)
                curLiContours.append({
                    'contour': curCanvasContour,
                    # 'contour': contour,
                    'count': 0
                });
                #按照当前的contour生成polygon，后面用来统计当前contour生成的polygon中点的个数
                # curPolygon = Polygon(contour)

                curPolygon = Polygon(curCanvasContour)
                curLiPolygon.append(curPolygon)
            
            #遍历数据点，然后遍历前面根据isoValue生成的polygon，判断当前数据点是否再polygon里面，在得话count加一
            for dot in dots:
                point = Point([dot['x'], dot['y']])
                for index_temp in range(len(curLiPolygon)):
                    polygon = curLiPolygon[index_temp]
                    if(polygon.contains(point) == True):
                        curLiContours[index_temp]['count'] += 1
            
            if (len(curLiContours) != 0):
                # 将contour和count信息以对象形式返回，且key是初始生成的各个isoValue
                mapIsovalueContours[str(curIsovalue)] = curLiContours
        return mapIsovalueContours, maxDensityPoints
        

class KDEHandler():
    geoInstance = getGeoInfo()

    def getXY(self, dotInfo):
        liX = []
        liY = []
        for i in range(len(dotInfo)):
            liX.append(dotInfo[i]['x'])
            liY.append(dotInfo[i]['y'])
        return np.array(liX), np.array(liY)
    
    def turpleToList(self, curTurpleData):
        curListData = list(curTurpleData)
        for item in curListData:
            curListData[curListData.index(item)] = list(item)
        return curListData

    def getAllClassDot(self, data):
        liAllDots = []
        for classId, dotsXYData in data.items():
            for i in range(len(dotsXYData)):
                liAllDots.append(dotsXYData[i])
        return liAllDots
    
    def computeKDE(self, data):
        # print('test data', data)
        estimator = KMeans(n_clusters=3)#构造聚类器
        # result = estimator.fit_predict(data)
        DistanceInstance = Distance()
        KDEContour = KDE()
        liCluster = [];
        liModifiedDots = []
        distanceCollect = [];
        contourPar = [];

        #定义密度场计算范围
        xmin = 0;
        xmax = 800;
        ymin = 0;
        ymax = 800;

        allDotsXYData = self.getAllClassDot(data)
        globalM1, globalM2 = self.getXY(allDotsXYData)
        globalZ1 = KDEContour.kdeCore(globalM1, globalM2, xmin, xmax, ymin, ymax)
        globalMaxDensityPoints = []
        proximityPoints = []

        for classId, dotsXYData in data.items():
            curProximityPoints = []
            curMaxDensityPoints, curLowDensityPoints = KDEContour.getGlobalMaxDensityPoint(globalZ1, dotsXYData)
            # print('len', len(curMaxDensityPoints))
            # print('curMaxDensityPoints', curMaxDensityPoints)
            if len(curMaxDensityPoints) > 3:
                proximityCentoridPoints = estimator.fit(curMaxDensityPoints).cluster_centers_.tolist()
                # print('curLowDensityPoints',curLowDensityPoints)
                curProximityPoints = curLowDensityPoints + proximityCentoridPoints
                # print('centroid', estimator.fit(curMaxDensityPoints).cluster_centers_.tolist())
            else:
                curProximityPoints = curLowDensityPoints + curMaxDensityPoints
            print('len', len(curMaxDensityPoints))
            if (len(curMaxDensityPoints) == 0):
                print('maxDensity points none')
            else:
                globalMaxDensityPoints.append(curMaxDensityPoints[math.floor(len(curMaxDensityPoints) / 2)])
            # print('curProximityPoints',curProximityPoints)
            proximityPoints.append({'classId': classId, 'curClassProximityPoints': curProximityPoints})
        # globalTransferContour, globalMaxDensityPoints = KDEContour.getContours(globalZ1, allDotsXYData)

        #对每个classId计算kde
        for classId, dotsXYData in data.items():
            mainIsovalue = 1e6
            stopCompare = False

            curDistance = DistanceInstance.distanceCompute(dotsXYData)
            m1, m2 = self.getXY(dotsXYData)
            liDots = KDEContour.listZip(m1, m2);

            Z1 = KDEContour.kdeCore(m1, m2, xmin, xmax, ymin, ymax);

            curDensity = list(Z1.ravel())
            curTransferDot = self.turpleToList(zip(list(m1), list(m2)))
            liModifiedDots.append(curTransferDot)

            # 生成初始的contour，返回的是以isovalue为key的对象
            # 每个key对应以当前isovalue生成的一个或多个contour以及该contour里面包含的点的数量
            transferContour, maxDensityPoints = KDEContour.getContours(Z1, dotsXYData)

            # print('transferC', transferContour)

            #将有getContours函数中提取的isoValue存放在liIsoValue中并排序
            liIsovalue = []
            mainContour = {}
            mainIsovalue = 1e6
            stopCompare = False

            for Isovalue_str in transferContour.keys():
                liIsovalue.append(float(Isovalue_str))
            liIsovalue = sorted(liIsovalue)
            print('liIsovalue', liIsovalue)
            mapBezierContour = {}
            mapIsoContourCount = {}
            
            preCount = len(dotsXYData)
            # print('preCount', preCount)
            preContour = []
            preIsovalue = -1e6
            isoCount = 0
            
            for Isovalue in liIsovalue:
                maxCount = -1e6
                maxIsovalue = -1e6
                maxContour = []
                liNewContour = []
                liNewCount = []

                isoCount += 1
                Isovalue = str(Isovalue)
                liContour = transferContour[Isovalue]

                # 在每个isoValue下找到当前isovalue生成的contour中count最多的contour，并且将其放入当前isovalue下的 liNewContour和liNewCount中
                for temp in range(len(liContour)):
                    tempContour = liContour[temp]['contour']
                    tempCount = liContour[temp]['count']
                    if (maxCount < tempCount):
                        maxCount = tempCount
                        maxContour = tempContour
                        maxIsovalue = Isovalue
                    
                    beginPos = tempContour[0]
                    endPos = tempContour[-1]

                    if(abs(beginPos[0] - endPos[0]) > 10 or abs(beginPos[1] - endPos[1]) > 10):
                        continue
                    liNewContour.append(tempContour)
                    liNewCount.append(tempCount)
                # print('maxContour', maxContour)
                # preCount为当前类所以的点的数量，maxCount为当前isoValue生成的众多contour中点数量最多的contour的点数量
                # 只选择其中最大的一个contour的点数量是因为如果算两个contour的总和的话，没有骤减继续比较时应该选取哪个contour就成了一个问题
                # 进行了比较precount - maxCount > 点数量的87%说明已经发生了骤减，少了13%的点，可以选择外层的contour，
                # 如果没有的话，说明maxCount的点很多很多，选取这个contour当前isoValue生成的众多contour的代表也是可以的
                # print('maxContour', maxContour)
                # print('preCount', preCount)
                # print('maxCount', maxCount)
                
                if(stopCompare == False):
                    if((preCount - maxCount) > int(preCount * 0.13)):
                        # print('aaa')
                        if len(preContour) == 0:
                            mainContour = maxContour
                        else:
                            mainContour = preContour
                        print('maincontour', mainContour)
                        mainIsovalue = preIsovalue
                        stopCompare = True
                    else:
                        preContour = maxContour
                        print('aaa preContour', preContour)
                        preIsovalue = maxIsovalue

                if (len(liNewContour) > 0):
                    mapBezierContour[Isovalue] = liNewContour;
                    mapIsoContourCount[Isovalue] = liNewCount

            # print('maincontour', mainContour)
            curCentroid = self.geoInstance.getCentroid(mainContour)
        
            liCluster.append({
                'classId': classId,
                'dots': liDots,
                'centroid': curCentroid,
                'transferDots': curTransferDot,
                'density': curDensity,
                'minDensity': Z1.ravel().min(),
                'maxDensity': Z1.ravel().max(),
                'distance': curDistance,
                'contours': mapBezierContour,   
                'counts': mapIsoContourCount,
                'maincontour': mainContour,
                'mainIsovalue': mainIsovalue,
                'maxDensityPoints': maxDensityPoints
            })
        return liModifiedDots, {'clusters': liCluster, 'canvasRange': [xmin, xmax, ymin, ymax]}, globalMaxDensityPoints, proximityPoints

