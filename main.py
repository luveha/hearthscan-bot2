import praw
from praw.models import Message
import time
from time import sleep, strftime, localtime
import json
import string
from loadJson import *

#Sleep time in seconds
sleep_time = (120)
#Opening JSON file
cards = loadJson("data/cards")
constants = loadJson("data/constants")
keys = loadJson("credentials")

reddit = praw.Reddit(
    client_id= keys['client_id'],
    client_secret= keys['client_secret'],
    password= keys['password'],
    user_agent= keys['user_agent'],
    username= keys['username'],
)
# Needs to be false to print "reddit.user.me()"
reddit.read_only = False
responseList = []
subreddit = reddit.subreddit(keys['subreddit'])
print(reddit.user.me())

Nuller = "null"

def response_formatting(x):
    topDeckID = x['name'].lower().replace(" ", "-")
    #Needs both capword and tilte since title capitalized after -
    wikiID = string.capwords(x['name'].lower()).replace(" ", "_").title().replace('_The','_the')
    #x['hearthpwnID'] where 2 is
    returnVal = f"""* [{x['name']}]({x['image']}) {x['class']} {x['type']} {x['rarity']} {constants['sets'][x['set']]['stringShort']} ^[HP](https://www.hearthpwn.com/cards/2), ^[TD](https://www.hearthstonetopdecks.com/cards/{topDeckID}/), ^[W](https://hearthstone.wiki.gg/wiki/{wikiID}) \n\n {x['cost']}"""
    if x['type'] == 'Minion':
        returnVal += f"/{x['atk']}/{x['hp']}"
    elif x['type'] == 'Weapon':
        if x['atk'] != Nuller:
            returnVal += f"/{x['atk']}/{x['hp']}"
        else:
            returnVal += f"/-/{x['hp']}"
    elif x['type'] == "Spell" or x['type'] == "Hero" or x['type'] == "Hero Power":
        returnVal += f"/-/-"
    elif x['type'] == "Location":
        returnVal += f"/-/{x['hp']}"
    if x['subType'] != Nuller:
        returnVal += f" {x['subType']}"
    if x['desc'] != Nuller:
        returnVal += f" | {x['desc']}"
    return returnVal

def check_inbox():
    print("Running - Inbox")
    try:
        for msg in reddit.inbox.unread(limit=50):
            msg_body = msg.body.lower()
            max_counter = 0
            for i in cards:
                if max_counter >= 7:
                    break
                if f"[[{cards[i]['name'].lower()}]]" in msg_body:
                    max_counter += 1
                    responseList.append(response_formatting(cards[i]))
            response = ""
            for z in responseList:
                response += z + "\n\n"
            try:
                respond(msg, response)
                msg.mark_read()
            except Exception as e:
                continue
    except Exception as e:
        print("ERROR ERROR error")
def check_subreddit():
    for comment in subreddit.stream.comments(skip_existing=True):
        if not comment.saved and comment.author !=  keys['username']:
            response_list = []
            max_counter = 0
            comment_body = comment.body.lower().replace('\\','')
            for i in cards:
                if max_counter >= 7:
                    break
                if f"[[{cards[i]['name'].lower()}]]" in comment_body:
                    max_counter += 1
                    response_list .append(response_formatting(cards[i]))
            response = ""
            if response_list:
                response = "\n\n".join(response_list)
                comment.reply(response)
            comment.save()
        else:
            comment.save()

#Respond function
def respond(msg_to_respond, response):
    try:
        msg_to_respond.reply(body=response)
    except Exception as e:
        print(f"\t### ERROR - COULDN'T REPLY TO MESSAGE.\n\t{e}")

times = 0
#Run the bot
while True:
    #Something to run
    #check_inbox()
    print(times)
    check_subreddit()
    times += 1
    #Time to check again
    sleep(sleep_time)
    