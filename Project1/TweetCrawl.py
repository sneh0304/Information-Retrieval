import tweepy
import json
import jsonpickle

# load Twitter API credentials

with open('twitter_credentials.json') as cred_data:
	info = json.load(cred_data)
consumer_key = info['CONSUMER_KEY']
consumer_secret = info['CONSUMER_SECRET']
access_key = info['ACCESS_KEY']
access_secret = info['ACCESS_SECRET']

def get_all_tweets(screen_name):

    # Authorization and initialization

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialization of a list to hold all Tweets

    all_the_tweets = []

    # We will get the tweets with multiple requests of 200 tweets each

    new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=1170868243927617537)

    # saving the most recent tweets

    all_the_tweets.extend(new_tweets)

    #print (all_the_tweets)

    # save id of 1 less than the oldest tweet

    oldest_tweet = all_the_tweets[-1].id - 1

    # grabbing tweets till none are left

    while len(new_tweets) > 0:
    	# The max_id param will be used subsequently to prevent duplicates
    	new_tweets = api.user_timeline(screen_name=screen_name,
    	count=200, max_id=oldest_tweet)
    
    	# save most recent tweets
    
    	all_the_tweets.extend(new_tweets)
    
    	# id is updated to oldest tweet - 1 to keep track
    
    	oldest_tweet = all_the_tweets[-1].id - 1
    	print ('...%s tweets have been downloaded so far' % len(all_the_tweets))
    
    with open(screen_name+'_tweets1.json', 'a', encoding='utf8') as tweets:
        for tweet in all_the_tweets:
            tweets.write(jsonpickle.encode(tweet._json, unpicklable=False) + ',\n')

if __name__ == '__main__':

	get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))