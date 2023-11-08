import json
from loadJson import *

cards = loadJson('data/allData')
constants = loadJson('data/constants')

def classConvert(i):
    try:
        classes = i['multiClassGroup'].split('/')    
        for h in constants['classes']:
            z = 0
            while z < len(classes):
                if classes[z].lower() == h.lower():
                    classes[z] = constants['classes'][h]
                z += 1
        printString = ""
        for v in classes:
            printString += v + "/"
        return printString.rpartition('/')[0]
    except Exception as e:
        try:
            for h in constants['classes']:
                if i['playerClass'].lower() == h.lower():
                    return constants['classes'][h]
        except Exception as e:
            return "null"
def subtype(i):
    try:
        string = i['race'] + "/" + i['otherRaces'][0] 
        return string
    except Exception as e:
        try:
            string = i['race'] 
            return string
        except Exception as e:
            try:
                string = i['spellSchool']
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
        string = i['rarity']
        return string
    except Exception as e:
        try:
            if i['elite'] == True:
                string = "elite"
                return string
        except Exception as e:
            return "null"
    
def cleanUp(i,v):
    try:
        if nullTest(i,v) == "null":
            return "null"
        to_remov = {'\\n': ' ','<i>': '','</i>': '','[x]': '','<b>': '', '</b>': '','{0}': '','{1}': '','"': "'",'@ ( left!)':'',"@ (Ready!)":'','$':'','\\': ''}
        string = i[v]
        for char in to_remov.keys():
            string = string.replace(char,to_remov[char])
        return string
    except Exception as e:
            return "null"
def durORhp(i):
    try:
        if nullTest(i,'health') != "null":
            return i['health']
        elif nullTest(i,'durability') != "null":
            return i['durability']
        return "null"
    except Exception as e:
            return "null"
def toImage(i):
    try:
        start = "https://cards.hearthpwn.com/enUS/"
        end = ".png"
        return start + i + end
    except Exception as e:
            return "null"
#Defines
x = '{ }'
z = json.loads(x)
v = []
#Removing things like prologue etc.
remove = ['prologue']
#Gets short hands from sets
sets = []
for h in constants['sets']:
    sets.append(constants['sets'][h]['code'])
#Gets full names from sets
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
                        dictionary = {
                            "id": f"{nullTest(i,'cardId')}",
                            "name": f"{nullTest(i,'name')}",
                            "class": f"{classConvert(i)}",
                            "atk": nullTest(i,'attack'),
                            "hp": durORhp(i),
                            "cost": nullTest(i,'cost'),
                            "type": f"{i['type']}",
                            "subType": f"{subtype(i)}",
                            "image": f"{toImage(i['cardId'])}",
                            "set": f"{i['cardSet']}",
                            "rarity": f"{rarityTest(i)}"
                        }
                        z[f"{i['name'].lower()}"] = dictionary
            except IndexError: #Handling known erros
                continue
            except KeyError:
                continue
            except Exception as e: #Print errors if new ones arrives
                print(i['cardId'], type(e).__name__)
                continue
            
 
with open("data/cards.json", "w") as f3:
    f3.write(json.dumps(z, indent = 4))
f3.close()