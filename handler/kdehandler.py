import math;
import numpy as np;
from scipy import stats;

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
    
    def kdeCore(self, m1, m2, xmin, xmax, ymin, ymax):
        X, Y = np.mgrid[xmin:xmax:800j, ymin:ymax:800j]
        # print('x', X)
        # print('y', Y)
        positions = np.vstack([X.ravel(), Y.ravel()]);
        values = np.vstack([m1, m2]);
        kernel = stats.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        return np.rot90(Z)
        

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
            curDistance = DistanceInstance.distanceCompute(dotsXYData)
            m1, m2 = self.getXY(dotsXYData)
            # print('m1', m1)
            liDots = KDEContour.listZip(m1, m2);
            Z1 = KDEContour.kdeCore(m1, m2, xmin, xmax, ymin, ymax);
            curDensity = self.turpleToList(zip(list(m1), list(m2)))
            liModifiedDots.append(curDensity)
            liCluster.append({
                'classId': classId,
                'dots': liDots,
                'density': curDensity,
                'minDensity': Z1.ravel().min(),
                'maxDensity': Z1.ravel().max(),
                'distance': curDistance
            })
        return liModifiedDots, {'clusters': liCluster, 'canvasRange': [xmin, xmax, ymin, ymax]}

DistanceInstance = Distance()