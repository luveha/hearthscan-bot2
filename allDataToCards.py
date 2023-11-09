import json
from loadJson import *

cards = loadJson('data/allData')
constants = loadJson('data/constants')

def classConvert(i):
    classes = i.get('multiClassGroup', None)
    class1 = i.get('playerClass', None)
    if classes != None:
        classes = classes.split('/')
        for h in classes:
            if not (constants['classes'].get(h) is None):
                classes[classes.index(h)] = constants['classes'].get(h)
        return '/'.join(classes)
    elif not(constants['classes'].get(class1) is None):
        return constants['classes'].get(class1)
    else:
        return "null"

def subtype(i):
    race = i.get('race',None)
    otherRace = i.get('otherRaces',None)
    spellSchool = i.get('spellSchool',None)
    if otherRace != None:
        return race + '/' + '/'.join(otherRace)
    elif race != None:
        return race
    elif spellSchool != None:
        return spellSchool
    else:
        return "null"

def nullTest(i,v):
    return i.get(v, "null")

def collectableTest(i):
    if i.get("collectible", "null") != "null":
        return True
    else:
        return False


def cleanUp(i,v):
    try:
        if nullTest(i, v) == "null":
            return "null"
        to_remove = {'\\n': ' ', '<i>': '', '</i>': '', '[x]': '', '<b>': '', '</b>': '', '{0}': '', '{1}': '', '"': "'", '@ ( left!)': '', "@ (Ready!)": '', '$': '', '\\': '', '_': ' ',
                    '</I>':'','   ': ' ','  ':' ','@ |4(copy, copies)':'1 copy'}
        string = i[v]
        for char in to_remove:
            string = string.replace(char, to_remove[char])
        return string
    except Exception as e:
        return "null"

def durORhp(i):
    try:
        if 'health' in i:
            return i['health']
        elif 'durability' in i:
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

#Removing things like adventure cards.
remove = ['prologue']

#Gets short hands from sets
sets = [constants['sets'][h]['code'] for h in constants['sets']]
    
#Gets full names from sets
names = [constants['sets'][h]['name'] for h in constants['sets']]

#Running the test
for k in cards:
    if k in names:
        for i in cards[k]:
            try:
                if i['cardId'].split('_')[1].lower() not in remove:
                    if i['type'] != "Enchantment" and (i['cardId'].split('_')[0].upper() in sets or i['cardSet'] in {'Core','Legacy'}):
                        dictionary = {
                            "id": f"{nullTest(i,'cardId')}",
                            "name": f"{nullTest(i,'name')}",
                            "class": f"{classConvert(i)}",
                            "atk": nullTest(i,'attack'),
                            "hp": durORhp(i),
                            "cost": nullTest(i,'cost'),
                            "desc": cleanUp(i,'text'),
                            "type": f"{i['type']}",
                            "subType": f"{subtype(i)}",
                            "image": f"{toImage(i['cardId'])}",
                            "set": f"{i['cardSet']}",
                            "rarity": f"{nullTest(i,'rarity')}",
                            "collectable": f"{collectableTest(i)}"
                        }
                        if i['name'].lower() not in z:
                            z[i['name'].lower()] = dictionary
                        if i['cardSet'] == 'Core':
                            z[f"{i['name'].lower()} ({z[i['name'].lower()]['set'].lower()})"] = z[i['name'].lower()]
                            z[i['name'].lower()] = dictionary
                        elif i['cardSet'] != 'Unknown' and z['cardSet'] != i['cardSet']:
                            z[f"{i['name'].lower()} ({i['cardSet'].lower()})"] = dictionary
            except IndexError: #Handling known erros
                continue
            except KeyError:
                continue
            except Exception as e: #Print errors if new ones arrives
                print(i['cardId'], type(e).__name__)
                continue

with open("data/cards.json", "w") as f3:
    json.dump(z, f3, indent=4)