import json

twitter_cred = dict()

twitter_cred['CONSUMER_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
twitter_cred['CONSUMER_SECRET'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
twitter_cred['ACCESS_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
twitter_cred['ACCESS_SECRET'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
    
#This .py file will create will create a twitter_credentials.json file, which is being used in tweet crawl