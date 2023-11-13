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
minions = loadJson("minions")
anomalies = loadJson("anomaly")
heroes = loadJson("constants")
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
endMessage = " \n\n^(Call) ^me ^with ^up ^to ^7 ^[[cardname]]."
subreddit = reddit.subreddit(keys['subreddit'])
print(reddit.user.me())

def response_formatting(x):
    #Test if it is a minion
    if x.get('hp',None) != None:
        insert1 = x['image'].replace(')','\)')
        insert2 = x['wiki'].replace(')','\\)')
        nameTitel = x['name'].title()
        returnString = f"* **[{nameTitel}]({insert1})** Tier {x['tier']} "
        returnString +=  f" ^[W]({insert2})"
        returnString += " \n \n "
        returnString += f"{x['atk']}/{x['hp']} "
        if x['tribe'] != None:
             returnString += x['tribe'] + " "
        if x['desc'] != None:
            returnString += "| " + x['desc']
        return returnString
    if x.get('isAnom',None) == True:
        returnString = f"* **[{x['name']}]({x['image']})** "
        returnString +=  f" ^[W]({x['wiki']})"
        returnString += " \n \n "
        returnString += x['desc']
        return returnString
    if x.get('heropower',None) != None:
        heroLink = "https://hearthstone.wiki.gg/wiki/Battlegrounds/" + x['name'].replace(' ','_')
        heroPowerLink = "https://hearthstone.wiki.gg/wiki/Battlegrounds/" + x['heropower'].replace(' ','_')
        returnString = f"* **[{x['name'].title()}]({heroLink})** "
        returnString += " \n \n "
        returnString += f"Hero Power: **[{x['heropower']}]({heroPowerLink})** | {x['desc']}"
        return returnString

def check_submission():
    for submission in subreddit.stream.submissions(skip_existing=True):
        if not submission.saved:
            response_list = []
            max_counter = 0
            submission_body = submission.selftext.lower().replace('\\','')
            for i in minions:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in submission_body:      
                    max_counter += 1
                    response_list.append(response_formatting(minions[i]))
            for i in anomalies:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in submission_body:
                    max_counter += 1
                    response_list.append(response_formatting(anomalies[i]))
            for i in heroes:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in submission_body or f"[[{heroes[i].get('altName','neverever2321').lower()}]]" in submission_body:
                    max_counter += 1
                    response_list.append(response_formatting(heroes[i]))
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
            for i in minions:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in comment_body:
                    max_counter += 1
                    response_list.append(response_formatting(minions[i]))
            for i in anomalies:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in comment_body:
                    max_counter += 1
                    response_list.append(response_formatting(anomalies[i]))
            for i in heroes:
                if max_counter >= 7:
                    break
                if f"[[{i.lower()}]]" in comment_body or f"[[{heroes[i].get('altName','neverever1412').lower()}]]" in comment_body:
                    max_counter += 1
                    response_list.append(response_formatting(heroes[i]))
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
    
    t1.start()
    t2.start()