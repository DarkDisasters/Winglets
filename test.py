import Winglets

import json

dataDict = {}
f = open('./testFile.json', 'r')
dataDict = json.loads(f.read())
# print('dataDict', dataDict)
# draw(dataDict['dots'], ['#d7191c', '#fdae61', '#ffffbf', '#abdda4', '#2b83ba'])
dataArray = []
for curKey in dataDict['dots'].keys():
    curArrDictData = dataDict['dots'][curKey]
    curKeyArr = []
    for i in range(len(curArrDictData)):
        curKeyArr.append([curArrDictData[i]['x'], curArrDictData[i]['y']])
    dataArray.append(curKeyArr)
# print('dataArray', dataArray)
Winglets.draw(dataArray)
# draw(dataDict['dots'], ['#d7191c', '#fdae61', '#abdda4','#2b83ba'])