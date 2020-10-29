import math;

class DistanceOperation():
    def getDifClassDotDistance(self, dot1, dot2):
        return math.sqrt((dot1[0] - dot2[0])*(dot1[0] - dot2[0]) + (dot1[1] - dot2[1])*(dot1[1] - dot2[1]))

class WingletsStepHandler():
    m_mapDisMatrix = {}
    m_mapClassIdDotIndexSihouttle = {}
    m_mapClassIdMaxMinSI = {}
    m_mapClassIdDotIndexSensitivity = {}

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

            
