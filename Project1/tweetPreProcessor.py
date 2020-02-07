import json
import preprocessor as tpp

with open(input("Enter the file name you want to process:- "), 'r') as jsonFile:
    tweets = json.load(jsonFile)


US = ['realDonaldTrump', 'andersoncooper', 'BarackObama', 'ewarren', 'HillaryClinton', 'KamalaHarris', 'JoeBiden', 'PeteButtigieg', 'TulsiGabbard']
IND =['ArvindKejriwal', 'ChouhanShivraj', 'narendramodi', 'NitishKumar', 'RahulGandhi', 'ravishndtv', 'myogiadityanath', 'ShashiTharoor']
BRZ =['jairbolsonaro', 'LucianoHuck', 'MarinaSilva', 'MichelTemer', 'paulocoelho', 'alvarodias_', 'DaniloGentili', 'Haddad_Fernando', 'majorolimpio']

months = {
    'Jan':'1',
    'Feb':'2',
    'Mar':'3',
    'Apr':'4',
    'May':'5',
    'Jun':'6',
    'Jul':'7',
    'Aug':'8',
    'Sep':'9',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
}

for tweet in tweets:
    #id = tweet['id']
    poi_name = tweet['user']['screen_name']
    poi_id = tweet['user']['id']
    verified = tweet['user']['verified']
    country = ' '
    replied_to_tweet_id = tweet['in_reply_to_status_id']
    replied_to_user_id = tweet['in_reply_to_user_id']
    tweet_text = tweet['text']
    if replied_to_user_id is None:
        reply_text = ''
    else:
        reply_text = tweet_text
    tweet_lang = tweet['lang']
    hashtags = ''
    mentions = ''
    tweet_urls = ''
    tweet_emoticons = ''
    tweet_date = tweet['created_at']
    tweet_loc = tweet['coordinates']
    
    #if 'retweeted_status' in tweet:
    #    retweeted_status = tweet['retweeted_status']
    #    isRetweet = True
    #else:
    #    isRetweet = False
    parsedTweet = tpp.parse(tweet_text)
    
    splitTime = tweet_date.split()
    month = months[splitTime[1]]
    year = splitTime[5]
    day = splitTime[2]
    time = splitTime[3] #.split(':')[0]+':00:00'
    tweet_date = year + '-' + month + '-' + day + 'T' + time + 'Z'
    try:
        for temp in parsedTweet.hashtags:
            hashtags = hashtags + temp.match + ' '
        hashtags = hashtags.replace('#', '').strip(' ')
    except TypeError as te:
        hashtags = ''
    try:
        for temp in parsedTweet.mentions:
            mentions = mentions + temp.match + ' '
        mentions = mentions.replace('@', '').strip(' ')
    except TypeError as te:
        mentions = ''
    try:
        for temp in parsedTweet.urls:
            tweet_urls = tweet_urls + temp.match + ' '
        tweet_urls = tweet_urls.strip(' ')
    except TypeError as te:
        tweet_urls = ''
    try:
        for temp in parsedTweet.emojis:
            tweet_emoticons = tweet_emoticons + temp.match + ' '
    except TypeError as te:
        tweet_emoticons = ''
    try:
        for temp in parsedTweet.smileys:
            tweet_emoticons = tweet_emoticons + temp.match + ' '
        tweet_emoticons = tweet_emoticons.strip(' ')
    except TypeError as te:
        tweet_emoticons = ''
        
    if poi_name in US:
        country = 'USA'
    elif poi_name in IND:
        country = 'INDIA'
    elif poi_name in BRZ:
        country = 'BRAZIL'
    
    #tweet.clear()
    
    #tweet['id'] = id
    tweet['poi_name'] = poi_name
    tweet['poi_id'] = poi_id
    tweet['verified'] = verified
    tweet['country'] = country
    tweet['replied_to_tweet_id'] = replied_to_tweet_id
    tweet['replied_to_user_id'] = replied_to_user_id
    tweet['reply_text'] = reply_text
    tweet['tweet_text'] = tweet_text
    tweet['tweet_lang'] = tweet_lang
    if tweet_lang == 'en':
        tweet['text_en'] = tpp.clean(tweet_text)
    elif tweet_lang == 'hi':
        tweet['text_hi'] = tpp.clean(tweet_text)
    elif tweet_lang == 'pt':
        tweet['text_pt'] = tpp.clean(tweet_text)
    tweet['hashtags'] = hashtags
    tweet['mentions'] = mentions
    tweet['tweet_urls'] = tweet_urls
    tweet['tweet_emoticons'] = tweet_emoticons
    tweet['tweet_date'] = tweet_date
    tweet['tweet_loc'] = tweet_loc
    #if isRetweet:
    #   tweet['retweeted_status'] = retweeted_status

with open(poi_name+'_processedTweets.json', 'w') as f:
    json.dump(tweets, f)
