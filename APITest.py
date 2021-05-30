import Winglets
import json
import math

## Prepare Data
dataDict = {}
dataArray = []

f = open('./testFile.json', 'r')
dataDict = json.loads(f.read())

for curKey in dataDict['dots'].keys():
    curArrDictData = dataDict['dots'][curKey]
    curKeyArr = []
    for i in range(len(curArrDictData)):
        curKeyArr.append([curArrDictData[i]['x'], curArrDictData[i]['y']])
    dataArray.append(curKeyArr)

dataArrayTest = [
    [
        [2,3],
        [4,6],
        [4,5],
        [3,2],
        [6,5],
        [5,6],
        [1,2],
        [2,4]
    ]
]

dataArrayTest1 = [
                [
                    [-1.8467827164233757, -0.32359462877408124],
                    [-0.7646302727249497, -0.20169742403492624],
                    [-1.9490266612960963, -0.06872107311219157],
                    [-1.3985176033785436, -0.1394565639809605],
                    [-1.3192884234119042, 0.10408209719246732],
                    [-1.3008685617349127, -0.11898413174114462],
                    [-1.6118388742131056, -0.0825317789879439],
                    [-1.5480362947416044, 0.05477850586236834],
                    [-0.5204018281010724, -0.0064287721502440396],
                    [-1.3260328260134568, 0.0192675336368897],
                    [-1.3673899592569305, 0.02269954670743994],
                    [-1.8011236429571018, -0.2943896776054888],
                    [-1.2543877120537488, 0.013826796210314464],
                    [-1.7624360292903625, -0.13316404689552958],
                    [-2.1375891691271023, -0.10481913067508605],
                    [-1.0797929311491847, -0.006604367860836293],
                    [-1.9291588152470303, -0.05091304686418803],
                    [-2.070795065814931, 0.3587612219744936],
                    [-1.930805837668947, 0.19656344116061403],
                    [-1.7169013639633552, -0.19956534844023005],
                    [-1.030997817981172, 0.019922204353402286]
                ],
                [
                    [-0.5245786836857915, -0.009288441027319272],
                    [-1.5975406720074177, -0.164711589213956],
                    [-0.5238814441706277, -0.009185694875345709],
                    [-0.5376809953080502, -0.020119170111257204],
                    [-0.6552283992534788, -0.07678937700237982]
                ]
]

for i in range(len(dataArrayTest1)):
    for j in range(len(dataArrayTest1[i])):
        if dataArrayTest1[i][j][0] < 0:
            dataArrayTest1[i][j][0] *= -1
        if dataArrayTest1[i][j][1] < 0:
            dataArrayTest1[i][j][1] *= -1
        dataArrayTest1[i][j] = [dataArrayTest1[i][j][0] * 100, dataArrayTest1[i][j][1] * 100 ]

## Test Circle
# Winglets.drawCirlce(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)
# Winglets.drawCirlce(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#abdda4','#2b83ba'])


## Test Winglets
# Winglets.drawWinglets(dataArrayTest1, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)

# Winglets.drawWinglets(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
Winglets.drawWinglets(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawWinglets(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)
# Winglets.drawWinglets(dataArray, ['#d7191c', '#fdae61', '#abdda4'])

## Test CommonFate
# Winglets.drawCommonFate(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCommonFate(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCommonFate(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4'])

## Test Proximity
# Winglets.drawProximity(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawProximity(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])