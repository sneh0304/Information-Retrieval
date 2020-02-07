import textblob as tb
from nltk.corpus import stopwords
import os
import json
import re
import string
from googletrans import Translator
#import time

def remove_noise(text, stop_words = ()):
    cleaned_text = ''

    for token, tag in text.pos_tags:
        token = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", token)
        #token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        token = tb.Word(token).lemmatize(pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_text += token.lower().strip() + ' '
    return tb.TextBlob(cleaned_text.strip())

def main():
    stop_words = stopwords.words('english')
    
    count = 20
    total = 0
    pos = 0
    neg = 0
    neut = 0
    tr = Translator()
    
    with os.scandir('Tweets/yadavakhilesh_processedTweets/') as entries:
        for entry in entries:
            with open('Tweets/yadavakhilesh_processedTweets/' + entry.name, 'r') as jsonFile:
                tweets = json.load(jsonFile)
            print('file opened ', entry.name)
            cnt = 0
            for tweet in tweets:
                lang = tweet['lang']
                text = tweet['tweet_text']
                if lang != 'en':
                    try:
                        translated_text = tr.translate(text, dest = 'en').text
                        text = translated_text
                    except:
                        print('Not Translated')
                text = tb.TextBlob(text)
                text = remove_noise(text)
                print(cnt)
                cnt += 1
                if text.sentiment.polarity > 0:
                    tweet_sentiment = 'positive'
                    pos += 1
                elif text.sentiment.polarity < 0:
                    tweet_sentiment = 'negative'
                    neg += 1
                else:
                    tweet_sentiment = 'neutral'
                    neut += 1
                
                total += 1
                
                tweet['tweet_sentiment'] = tweet_sentiment
            
            with open('Tweets1/yadavakhilesh_processedTweets/'+ str(count) +'.json', 'w') as f:
                json.dump(tweets, f)
            
            count += 1
            #break
            #time.sleep(5)
    
    with open('Tweets1/yadavakhilesh_processedTweets/summary.txt', 'w') as s:
        s.writelines(['Positive sentiment count: ' + str(pos) + '\n', 'Negative sentiment count: ' + str(neg) + '\n', 'Neutral sentiment count: ' + str(neut) + '\n', 'Total sentiment count: ' + str(total) + '\n'])
    
if __name__ == '__main__':
    main()