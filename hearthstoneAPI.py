import requests
import json

#Load credentials
with open('credentials.json') as creds:
    keys = json.load(creds)

url = "https://omgvamp-hearthstone-v1.p.rapidapi.com/cards"

headers = {
	"X-RapidAPI-Key": keys['X-RapidAPI-Key'],
	"X-RapidAPI-Host": keys['X-RapidAPI-Host']
}

response = requests.get(url, headers=headers)

json_object = json.dumps(response.json(), indent=4)

with open("data/rawData.json", "w") as outfile:
    outfile.write(json_object)
#print(response.json())