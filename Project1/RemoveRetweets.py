import json

with open(input("Enter the file name you want to process:- "), 'r') as jsonFile:
    tweets = json.load(jsonFile)

for tweet in tweets:
    if 'retweeted_status' in tweet:
        tweets.remove(tweet)

with open(jsonFile.name.split('.')[0]+'_withoutRetweets.json', 'w') as f:
    json.dump(tweets, f)
