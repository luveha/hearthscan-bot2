import json

with open('data/allData.json') as f1:
    cards = json.load(f1)
with open('data/constants.json') as f2:
    constants = json.load(f2)

def classConvert(i):
    try:
        classes = i['multiClassGroup'].split('/')
        for h in constants['classes']:
            z = 0
            while z < 2:
                if classes[z].lower() == h.lower():
                    classes[z] = constants['classes'][h]
                z += 1
        return classes[0] + "/" + classes[1]
    except Exception as e:
        for h in constants['classes']:
            if i['playerClass'].lower() == h.lower():
                return constants['classes'][h]
def subtype(i):
    try:
        string = '"' + i['race'] + "/" + i['otherRaces'][0] + '"'
        return string
    except Exception as e:
        try:
            string = '"' + i['race'] + '"'
            return string
        except Exception as e:
            try:
                string = '"' + i['spellSchool'] + '"'
                return string
            except Exception as e:
                return "null"
def nullTest(i,v):
    try:
        m = i[v]
        return m
    except Exception as e:
        return "null"
def rarityTest(i):
    try:
        string = '"' + i['rarity'] + '"'
        return string
    except Exception as e:
        try:
            if i['elite'] == True:
                string = '"' + "elite" + '"'
                return string
        except Exception as e:
            return "null"
    
def cleanUp(i,v):
    if nullTest(i,v) == "null":
        return "null"
    to_remov = {'\\n': ' ','<i>': '','</i>': '','[x]': '','<b>': '', '</b>': '','{0}': '','{1}': '','"': "'",'@ ( left!)':'',"@ (Ready!)":'','$':''}
    string = i[v]
    for char in to_remov.keys():
        string = string.replace(char,to_remov[char])
    return '"' + string + '"'
def durORhp(i):
    if nullTest(i,'health') != "null":
        return i['health']
    elif nullTest(i,'durability') != "null":
        return i['durability']
    return "null"
def toImage(i):
    start = "https://cards.hearthpwn.com/enUS/"
    end = ".png"
    return start + i + end

#Defines
x = '{ }'
z = json.loads(x)
v = []
#Removing things like prologue etc.
remove = ['prologue']
#Shorthand codes for sets
sets = []
for h in constants['sets']:
    sets.append(constants['sets'][h]['code'])
names = []
for h in constants['sets']:
    names.append(constants['sets'][h]['name'])
#Running the test
for k in cards:
    if k in names:
        for i in cards[k]:
            try:
                if i['cardId'].split('_')[1].lower() not in remove:
                    if i['type'] != "Enchantment" and i['cardId'].split('_')[0].upper() in sets:
                        y = f"""{{ "id": "{i['cardId']}", "name": "{i['name']}", "class": "{classConvert(i)}", "type": "{i['type']}", "subType": {subtype(i)},
                        "cost": {nullTest(i,'cost')}, "atk": {nullTest(i,'attack')},  "hp": {durORhp(i)}, "collectible": {str(nullTest(i,'collectible')).lower()}, "desc": {cleanUp(i,"text")},
                        "image": "{toImage(i['cardId'])}", "set": "{i['cardSet']}", "rarity": {rarityTest(i)}
                        }}"""
                        w = json.loads(y)
                        z[f"{i['name'].lower()}"] = w
            except KeyError:
                continue
 
with open("data/cards.json", "w") as f3:
    f3.write(json.dumps(z, indent = 4))
f3.close()