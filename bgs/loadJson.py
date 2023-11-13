import json

def loadJson(inputString):
    with open(f'{inputString}.json') as x:
        return json.load(x)