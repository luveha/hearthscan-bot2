import json
from loadJson import *

cards = loadJson('data/allData')
classes = loadJson('data/constants')

#Defines
v = []
newVar = ""
#Running the test
#all are sets
for i in cards:
    for t in cards[i]:
        try:
            newVar = t['cardId'].split('_')[0]
        except Exception as e:
            newVar = "null"
        if newVar not in v:
            v.append(newVar)
            
with open("data/setsData.json", "w") as f3:
    f3.write(json.dumps(v, indent = 4))
print(v)