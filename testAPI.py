import Winglets
import json

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


## Test Circle
# Winglets.drawCirlce(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'], False)
# Winglets.drawCirlce(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCirlce(dataDict['dots'], ['#d7191c', '#abdda4','#2b83ba'])


## Test Winglets
# Winglets.drawWinglets(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawWinglets(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
Winglets.drawWinglets(dataDict['dots'], ['#399939', '#D5241F', '#2073AA','#EF7D1B'], False)
# Winglets.drawWinglets(dataArray, ['#d7191c', '#fdae61', '#abdda4'])

## Test CommonFate
# Winglets.drawCommonFate(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCommonFate(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawCommonFate(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4'])

## Test Proximity
# Winglets.drawProximity(dataArray, ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])
# Winglets.drawProximity(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])