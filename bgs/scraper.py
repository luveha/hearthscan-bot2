import string
import requests
from bs4 import BeautifulSoup

def imageLink(nameId,cardId):
    webString = "https://hearthstone.wiki.gg/wiki/Battlegrounds/"
    webString += nameId.replace(' ','_') + "#/media/File:" + cardId + "_Battlegrounds.png"
    
    return webString
    

def wikiLink(nameId):
    webString = "https://hearthstone.wiki.gg/wiki/Battlegrounds/"
    theCardWeb = webString + nameId.replace(' ','_')
    
    return theCardWeb

def getTier(nameId):
    try:
        theCardWeb = wikiLink(nameId)
        
        r = requests.get(theCardWeb)
        soup = BeautifulSoup(r.content, "html.parser")

        #Finds where the tier is stated
        statsBox = soup.find("div", {"data-source": "bgTier"})
        theTierBox = statsBox.find("div", {"class": "pi-data-value pi-font"})
        tier = theTierBox.text
        
        return int(tier)
    except AttributeError as e:
        return "manualGetTier"
