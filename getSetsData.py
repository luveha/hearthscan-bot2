import json

with open('data/allData.json') as f1:
    cards = json.load(f1)
with open('data/constants.json') as f2:
    classes = json.load(f2)

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