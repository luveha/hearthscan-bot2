import praw
from praw.models import Message
import time
from time import sleep, strftime, localtime
import json
import string
from loadJson import *
import threading

#Sleep time in seconds
sleep_time = (5)
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
endMessage = " \n\n^(Call/)^[PM](https://www.reddit.com/message/compose/?to=hearthscan-bot2) ^me ^with ^up ^to ^7 ^[[cardname]]."
subreddit = reddit.subreddit(keys['subreddit'])
print(reddit.user.me())

def response_formatting(x):
    topDeckID = x['name'].lower().replace(" ", "-")
    #Needs both capword and tilte since title capitalized after -
    wikiID = string.capwords(x['name'].lower()).replace(" ", "_").title().replace('_The','_the')
    returnString = f"* **[{x['name']}]({x['image']})** {x['class']} {x['type']} "
    if x['rarity'] != None:
        returnString += f" {x['rarity']}"
    returnString += f" {constants['sets'][x['set']]['stringShort']} "
    #returnString += " ^[HP](https://www.hearthpwn.com/cards/2)," needs to fixed at some point
    returnString += f" ^[TD](https://www.hearthstonetopdecks.com/cards/{topDeckID}/),"
    returnString +=  f" ^[W](https://hearthstone.wiki.gg/wiki/{wikiID})"
    returnString += " \n \n "
    if x['type'] != 'Portal':
        returnString += str(x['cost'])
    else:
        returnString += '"' + x['type'] + '"'
    if x['type'] == 'Minion':
        returnString += f"/{x['atk']}/{x['hp']}"
    elif x['type'] == 'Weapon':
        if x['atk'] != None:
            returnString += f"/{x['atk']}/{x['hp']}"
        else:
            returnString += f"/0/{x['hp']}"
    elif x['type'] == "Spell" or x['type'] == "Hero" or x['type'] == "Hero Power":
        returnString += f"/-/-"
    elif x['type'] == "Location":
        returnString += f"/-/{x['hp']}"
    if x['subType'] != None:
        returnString += f" {x['subType']}"
    if x['desc'] != None:
        returnString += f" | {x['desc']}"
    return returnString

def check_inbox():
    try:
        for msg in reddit.inbox.unread(limit=50):
            msg_body = msg.body.lower()
            max_counter = 0
            for i in cards:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in msg_body:
                    max_counter += 1
                    responseList.append(response_formatting(cards[i]))
            response = ""
            if response_list:
                response = "\n\n".join(response_list)
                response += endMessage
                respond(msg, response)
            msg.mark_read()
    except Exception as e:
        print("ERROR ERROR error")
def checker_inbox():
    while True:
        check_inbox()
        sleep(30)
def check_submission():
    for submission in subreddit.stream.submissions(skip_existing=True):
        if not submission.saved:
            response_list = []
            max_counter = 0
            submission_body = submission.selftext.lower().replace('\\','')
            for i in cards:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in submission_body:       
                    max_counter += 1
                    response_list.append(response_formatting(cards[i]))
            response = ""
            if response_list:
                response = "\n\n".join(response_list)
                response += endMessage
                submission.reply(response)
            submission.save()
        else:
            submission.save()
            
def check_subreddit():
    for comment in subreddit.stream.comments(skip_existing=True):
        if not comment.saved and comment.author !=  keys['username']:
            response_list = []
            max_counter = 0
            comment_body = comment.body.lower().replace('\\','')
            for i in cards:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in comment_body:       
                    max_counter += 1
                    response_list.append(response_formatting(cards[i]))
            response = ""
            if response_list:
                response = "\n\n".join(response_list)
                response += endMessage
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

#Run the bot
if True:
    #Checking
    t1 = threading.Thread(target=check_submission)
    t2 = threading.Thread(target=check_subreddit)
    t3 = threading.Thread(target=checker_inbox)
    
    t1.start()
    t2.start()
    t3.start()