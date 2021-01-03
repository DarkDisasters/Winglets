import Winglets

import json
dataDict = {}
f = open('./testFile.json', 'r')
dataDict = json.loads(f.read())
print('dddd')
print('dataDict', dataDict)

Winglets.draw(dataDict['dots'])

