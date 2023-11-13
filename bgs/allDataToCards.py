import json
from loadJson import *
from scraper import *

cards = loadJson('allData')

def nullTest(i,v):
    return i.get(v, None)

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
def getTribe(i):
    race = i.get('race',None)
    otherRace = i.get('otherRaces',None)
    if otherRace != None:
        return race + '/' + '/'.join(otherRace)
    elif race != None:
        return race
    else:
        return None
#Defs
x = '{ }'
z = json.loads(x)
v = json.loads(x)
runMinion = True
runAnomily = False
runHero = False

for k in cards['Battlegrounds']:
    try:
        if k.get('type',None) == 'Minion' and runMinion:
            if k['name'].lower() not in z:
                dictionary = {
                    "id": k['cardId'],
                    "name": k['name'],
                    "tribe": getTribe(k),
                    "atk": nullTest(k,'attack'),
                    "hp": nullTest(k,'health'),
                    "tier": getTier(k['name']),
                    "desc": cleanUp(k,'text'),
                    "wiki": wikiLink(k['name']),
                    "image": imageLink(k['name'],k['cardId'])
                }
                z[k['name'].lower()] = dictionary
            elif k['health'] == 2 * z[k['name'].lower()]['hp']:
                dictionary = {
                    "id": k['cardId'],
                    "name": f"{k['name']} (Golden)",
                    "tribe": getTribe(k),
                    "atk": nullTest(k,'attack'),
                    "hp": nullTest(k,'health'),
                    "tier": z[k['name'].lower()]['tier'],
                    "desc": cleanUp(k,'text'),
                    "wiki": wikiLink(k['name']) + "_(golden)",
                    "image": imageLink((k['name'] + "_(golden)"),k['cardId'])
                }
                z[f"{k['name'].lower()} (golden)"] = dictionary
            elif k['health'] * 2 == z[k['name'].lower()]['hp']:
                z[f"{k['name'].lower()} (golden)"] = z[k['name'].lower()]
                z[f"{k['name'].lower()} (golden)"]['name'] = z[f"{k['name'].lower()} (golden)"]['name'] + " (golden)"
                z[f"{k['name'].lower()} (golden)"]["wiki"] = wikiLink(k['name'] + "_(golden)"),
                z[f"{k['name'].lower()} (golden)"]["wiki"] = z[f"{k['name'].lower()} (golden)"]["wiki"][0]
                z[f"{k['name'].lower()} (golden)"]["image"] = imageLink((k['name'] + "_(golden)"),k['cardId'] + "_G")
                dictionary = {
                    "id": k['cardId'],
                    "name": k['name'],
                    "tribe": getTribe(k),
                    "atk": nullTest(k,'attack'),
                    "hp": nullTest(k,'health'),
                    "tier": getTier(k['name']),
                    "desc": cleanUp(k,'text'),
                    "wiki": wikiLink(k['name']),
                    "image": imageLink(k['name'],k['cardId'])
                }
                z[k['name'].lower()] = dictionary
        elif runAnomily and k['cardId'].split('_')[1].lower() == 'anomaly' and k.get('type',None) != 'Enchantment':
            if k['name'].lower() not in z:
                dictionary = {
                    "id": k['cardId'],
                    "name": k['name'],
                    "desc": cleanUp(k,'text'),
                    "wiki": wikiLink(k['name']),
                    "image": imageLink(k['name'],k['cardId']),
                    "isAnom": True
                }
                v[k['name'].lower()] = dictionary
    except KeyError as ke:
        continue
    except Exception as e:
        print(type(e).__name__)

if runMinion:
    with open("minions.json", "w") as f3:
        json.dump(z, f3, indent=4)
if runAnomily:
    with open("anomaly.json", "w") as f4:
        json.dump(v, f4, indent=4)