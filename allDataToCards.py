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
        return None

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
        return None

def nullTest(i,v):
    return i.get(v, None)

def collectableTest(i):
    if i.get("collectible", None) != None:
        return True
    else:
        return False


def cleanUp(i,v):
    try:
        if nullTest(i, v) == None:
            return None
        to_remove = {'\\n': ' ', '<i>': '', '</i>': '', '[x]': '', '<b>': '', '</b>': '', '{0}': '', '{1}': '', '"': "'", '@ ( left!)': '', "@ (Ready!)": '', '$': '', '\\': '', '_': ' ',
                    '</I>':'','   ': ' ','  ':' ','@ |4(copy, copies)':'1 copy'}
        string = i[v]
        for char in to_remove:
            string = string.replace(char, to_remove[char])
        return string
    except Exception as e:
        return None

def durORhp(i):
    try:
        if 'health' in i:
            return i['health']
        elif 'durability' in i:
            return i['durability']
        return None
    except Exception as e:
        return None

def toImage(i):
    start = "https://cards.hearthpwn.com/enUS/"
    end = ".png"
    return start + i + end

def toSet(i):
    if i['cardSet'] in {'Hall of Fame','Classic'}:
        return 'Legacy'
    else:
        return i['cardSet']

#Defines
x = '{ }'
z = json.loads(x)
v = []

#Removing things like adventure cards.
remove = ['prologue','a02','a01','a10','500d','027h','story']

#Gets short hands from sets
sets = [constants['sets'][h]['code'] for h in constants['sets']]
    
#Gets full names from sets
names = [constants['sets'][h]['name'] for h in constants['sets']]

#Running the test
for k in cards:
    if k in names:
        for i in cards[k]:
            try:
                if i['cardId'].split('_')[1].lower() not in remove and i['cardId'].split('_')[0].lower() not in remove and i['name'] != '???':
                    if i['type'] != "Enchantment" and (i['cardId'].split('_')[0].upper() in sets or i['cardSet'] in {'Core','Legacy','Hall of Fame','Classic'}):
                        dictionary = {
                            "id": nullTest(i,'cardId'),
                            "name": nullTest(i,'name'),
                            "class": classConvert(i),
                            "atk": nullTest(i,'attack'),
                            "hp": durORhp(i),
                            "cost": nullTest(i,'cost'),
                            "desc": cleanUp(i,'text'),
                            "type": i['type'],
                            "subType": subtype(i),
                            "image": toImage(i['cardId']),
                            "set": toSet(i),
                            "rarity": nullTest(i,'rarity'),
                            "collectable": collectableTest(i)
                        }
                        if i['name'].lower() not in z:
                            z[i['name'].lower()] = dictionary
                        elif i['cardSet'] == 'Core':
                            z[f"{i['name'].lower()} ({z[i['name'].lower()]['set'].lower()})"] = z[i['name'].lower()]
                            z[i['name'].lower()] = dictionary
                        elif i['cardSet'] != 'Unknown' and z[i['name'].lower()]['set'].lower() != toSet(i).lower():
                            z[f"{i['name'].lower()} ({toSet(i).lower()})"] = dictionary
                        elif z[i['name'].lower()]['set'].lower() == toSet(i).lower() and (i['type'] == 'Hero Power' or z[i['name'].lower()]['type'] == 'Hero Power'):
                            if z[i['name'].lower()]['type'] == 'Hero Power':
                                z[f"{i['name'].lower()} ({z[i['name'].lower()]['type'].lower()})"] = z[i['name'].lower()]
                                z[i['name'].lower()] = dictionary
                            elif i['type'] == 'Hero Power':
                                z[f"{i['name'].lower()} ({i['type'].lower()})"]
                                z[i['name'].lower()] = dictionar
            except IndexError: #Handling known erros
                continue
            except KeyError as e:
                continue
            except Exception as e: #Print errors if new ones arrives
                print(i['cardId'], type(e).__name__)
                continue

#Handling weird edge cases like the "untouchables" dormants like imp portals and purified dragon nest
for cards in z:
    if z[cards]['atk'] == 0 and z[cards]['hp'] == 1 and z[cards]['cost'] == 11:
        z[cards]['atk'] = None
        z[cards]['hp'] = None
        z[cards]['cost'] = None
        z[cards]['type'] = 'Portal'

with open("data/cards.json", "w") as f3:
    json.dump(z, f3, indent=4)