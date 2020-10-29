import math;
import numpy as np;
from scipy import stats;
from skimage import measure;

from shapely.geometry import Point;
from shapely.geometry import Polygon;

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
        dot = [dotxy[1], 100 - dotxy[0]]
        scale = 8
        return [scale * dot[0], scale * dot[1]] 

    def convert2Canvas(self, contour):
        newContour = []
        for dot in contour:
            scaleDot = self.dot2Canvas(dot)
            newContour.append(scaleDot)
        return newContour
    
    def kdeCore(self, m1, m2, xmin, xmax, ymin, ymax):
        X, Y = np.mgrid[xmin:xmax:800j, ymin:ymax:800j]
        # print('x', X)
        # print('y', Y)
        positions = np.vstack([X.ravel(), Y.ravel()]);
        values = np.vstack([m1, m2]);
        kernel = stats.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        return np.rot90(Z)

    def getContours(self, Z, dots):
        mapIsoValueContours = {}
        isoPosNum = 10
        baseValue = 1e-9
        liIsoValue = []
        minDensity = Z.ravel().min()
        maxDensity = Z.ravel().max()
        liIsoValue.append(1e-1)

        #根据设定的baseValue和isoPosNum按密度分段，将范围的每个值存入liIsoValue
        for i in range(isoPosNum):
            liIsoValue.append(baseValue + i * (maxDensity - baseValue)/isoPosNum)
        
        #遍历设定的密度范围的分段值
        for i in range(len(liIsoValue)):
            #按照当前的 isoValue 生成contours
            curContours = measure.find_contours(Z, liIsoValue[i])
            curIsoValue = liIsoValue[i]
            #存放转化后的contours以及增加的信息
            curLiContours = []
            curLiPolygon = []

            #遍历按照当前isoValue生成的contour,因为同一个值可能生成两个互补重叠的contour，参考等高线
            for n, contour in enumerate(curContours):
                contour = contour.tolist();
                if (len(contour) == 0):
                    continue
                #将当前的contour以及设定count为0，用来统计当前isoValue生成的contour里有多少个点
                curLiContours.append({
                    'contour': contour,
                    'count': 0
                });
                # 缩放，此处我注释了
                # curCanvasContour = self.convert2Canvas(contour)
                #按照当前的contour生成polygon，后面用来统计当前contour生成的polygon中点的个数
                curPolygon = Polygon(contour)
                curLiPolygon.append(curPolygon)
            
            #遍历数据点，然后遍历前面根据isoValue生成的polygon，判断当前数据点是否再polygon里面，在得话count加一
            for dot in dots:
                point = Point([dot['x'], dot['y']])
                for index_temp in range(len(curLiPolygon)):
                    polygon = curLiPolygon[index_temp]
                    if(polygon.contains(point)):
                        curLiContours[index_temp]['count'] += 1
            
            if (len(curLiContours) != 0):
                # 将contour和count信息以对象形式返回，且key是初始生成的各个isoValue
                mapIsoValueContours[str(curIsoValue)] = curLiContours
                # print('count', mapIsoValueContours[str(curIsoValue)][0]['count'])
        return mapIsoValueContours
        

class KDEHandler():
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

    def computeKDE(self, data):
        print('test data', data)
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

        #对每个classId计算kde
        for classId, dotsXYData in data.items():
            mainIsoValue = 1e6
            stopCompare = False

            curDistance = DistanceInstance.distanceCompute(dotsXYData)
            m1, m2 = self.getXY(dotsXYData)
            liDots = KDEContour.listZip(m1, m2);

            Z1 = KDEContour.kdeCore(m1, m2, xmin, xmax, ymin, ymax);

            curDensity = list(Z1.ravel())
            curTransferDot = self.turpleToList(zip(list(m1), list(m2)))
            liModifiedDots.append(curTransferDot)

            transferContour = KDEContour.getContours(Z1, dotsXYData)

            #将有getContours函数中提取的isoValue存放在liIsoValue中并排序
            liIsoValue = []
            mainContour = {}
            mainIsovalue = 1e6
            stopCompare = False

            for isoValue_str in transferContour.keys():
                liIsoValue.append(float(isoValue_str))
            liIsoValue = sorted(liIsoValue)
            
            preCount = len(dotsXYData)
            preContour = []
            preIsoValue = -1e6
            isoCount = 0

            for isoValue in liIsoValue:
                maxCount = -1e6
                maxIsoValue = -1e6
                maxContour = []
                liNewContour = []
                liNewCount = []
                mapBezierContour = {}
                mapIsoContourCount = {}

                isoCount+= 1
                isoValue = str(isoValue)
                liContour = transferContour[isoValue]

                for temp in range(len(liContour)):
                    tempContour = liContour[temp]['contour']
                    tempCount = liContour[temp]['count']
                    if (maxCount < tempCount):
                        maxCount = tempCount
                        maxContour = tempContour
                        maxIsoValue = isoValue
                    
                    beginPos = tempContour[0]
                    endPos = tempContour[-1]

                    if(abs(beginPos[0] - endPos[0]) > 10 or abs(beginPos[1] - endPos[1]) > 10):
                        continue
                    liNewContour.append(tempContour)
                    liNewCount.append(tempCount)
                
                # preCount为当前类所以的点的数量，maxCount为当前isoValue生成的众多contour中点数量最多的contour的点数量
                # 只选择其中最大的一个contour的点数量是因为如果算两个contour的总和的话，没有骤减继续比较时应该选取哪个contour就成了一个问题
                # 进行了比较precount - maxCount > 点数量的87%说明已经发生了骤减，少了13%的点，可以选择外层的contour，
                # 如果没有的话，说明maxCount的点很多很多，选取这个contour当前isoValue生成的众多contour的代表也是可以的
                if(stopCompare == False):
                    if((preCount - maxCount) > int(preCount * 0.13)):
                        mainContour = preContour
                        mainIsovalue = preIsoValue
                        stopCompare = True
                    else:
                        preContour = maxContour
                        preIsoValue = maxIsoValue

                if (len(liNewContour) > 0):
                    mapBezierContour[isoValue] = liNewContour;
                    mapIsoContourCount[isoValue] = liNewCount

            
            liCluster.append({
                'classId': classId,
                'dots': liDots,
                'density': curDensity,
                'minDensity': Z1.ravel().min(),
                'maxDensity': Z1.ravel().max(),
                'distance': curDistance,
                'contours': mapBezierContour,
                'counts': mapIsoContourCount,
                'maincontour': mainContour,
                'mainisovalue': mainIsoValue
            })
        return liModifiedDots, {'clusters': liCluster, 'canvasRange': [xmin, xmax, ymin, ymax]}

