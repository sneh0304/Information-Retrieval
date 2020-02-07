from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
import json
import urllib.request
import time

class BasicView(View):
    def get(self, request):
        # return JsonResponse({'foo': 'bar'})
        return JsonResponse(['foo'], safe=False)


class CustomView(View):
    def get(self, request):
        dummy_dict = {
            'foo': 'bar',
            'goo': 'car',
            'hoo': 'dar',
            'ioo': 'ear',
            'loo': 'aar'
        }
        return JsonResponse(dummy_dict)

class HomeView(View):
    def get(self, request):
        output = []
        # print (request.GET['search'])
        query = request.GET['search']
        query = query.split(' ')
        query = ' '.join(query)
        query = urllib.parse.quote(query)
        # import pdb; pdb.set_trace()
        # http://localhost:8983/solr/all3/select?defType=edismax&fl=id%2Cscore&q=(corruption)&qf=tweet_text&stopwords=true&rows=10&wt=json
        start_time = time.time()
        inurl = 'http://3.135.17.6:8984/solr/LM/select?defType=edismax&fl=id%2Ctweet_text%2Cpoi_name%2Cretweet_count%2Cfavorite_count%2Ctweet_date%2Cverified%2Ccountry%2Clang%2Ctweet_sentiment%2Ctopic%2Cverfied&q=(' + query +')&qf=text_en%20text_pt%20text_hi&stopwords=true&rows=1500&wt=json'
        data = urllib.request.urlopen(inurl).read()
        timeTaken = time.time() - start_time
        docs = json.loads(data.decode('utf-8'))['response']['docs']
        retrievedTweets = json.loads(data.decode('utf-8'))['response']['numFound']
        if len(docs) == 0:
            print ("no data")
            return JsonResponse(output, safe=False)

        for doc in docs:
            dict = {}
            for key in doc:
                if key == "tweet_text":
                    dict["text"] = doc[key][0]
                if key == "poi_name":
                    dict["name"] = doc[key][0]
                if key == "retweet_count":
                    dict["ret_count"] = doc[key][0]
                if key == "favorite_count":
                    dict["fav_count"] = doc[key][0]
                if key == "lang":
                    dict["language"] = doc[key][0]
                if key == "country":
                    dict["country"] = doc[key][0]
                if key == "tweet_sentiment":
                    dict["tweet_sentiment"] = doc[key][0]
                    if dict["tweet_sentiment"] == "negative":
                        dict["is_bg_red"] = True
                        dict["is_bg_green"] = False
                        dict["is_bg_white"] = False
                    elif dict["tweet_sentiment"] == "positive":
                        dict["is_bg_red"] = False
                        dict["is_bg_green"] = True
                        dict["is_bg_white"] = False
                    else:
                        dict["is_bg_red"] = False
                        dict["is_bg_green"] = False
                        dict["is_bg_white"] = True

                else:
                    dict[key] = doc[key]
                if key == "verified":
                    dict["verified"] = doc[key][0]
            if "topic" not in dict:
                dict["topic"] = [10]
            if "retrievedTweets" not in dict:
                dict["retrievedTweets"] = retrievedTweets
            if "timeTaken" not in dict:
                dict["timeTaken"] = round(timeTaken, 4)

            output.append(dict)

        return JsonResponse(output, safe=False)
