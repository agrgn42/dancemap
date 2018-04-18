# from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import json
import sys
import requests
import secrets # file that contains OAuth credentials
import nltk
from nltk.corpus import stopwords
import csv

consumer_key = secrets.CONSUMER_KEY
consumer_secret = secrets.CONSUMER_SECRET
access_token = secrets.ACCESS_KEY
access_secret = secrets.ACCESS_SECRET

#Code for OAuth starts
oauth = OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)
#Code for OAuth ends


CACHE_FNAME = 'twitter_cache.json'

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents_str = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents_str)
	cache_file.close()
except:
    CACHE_DICTION = {}


# generate unique identifier for each api request
def params_unique_combination(baseurl, params_d):
	alphabetized_keys = sorted(params_d.keys())
	results_keys=[]
	for k in alphabetized_keys:
		results_keys.append("{}-{}".format(k, params_d[k]))
	return baseurl + "_".join(results_keys)


def get_from_twitter(count=25):
    try:
        baseurl = "https://api.twitter.com/1.1/search/tweets.json"
        params_d = {}
        params_d["q"] = "dance"
        params_d["result_type"] = "recent"
        params_d["geocode"] = '45.4166,-75.7,1000km'
        params_d["count"] = count
        unique_identifier = params_unique_combination(baseurl, params_d)
        if unique_identifier in CACHE_DICTION:
            print('Getting cached Twitter data...')
            return CACHE_DICTION[unique_identifier]
        else:
            print('Making request for new Twitter data...')
            twitter_resp = oauth.get(baseurl, params=params_d)
            CACHE_DICTION[unique_identifier] = json.loads(twitter_resp.text)
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fwrite = open(CACHE_FNAME,'w')
            fwrite.write(dumped_json_cache)
            fwrite.close()
            return CACHE_DICTION[unique_identifier]
    except TypeError:
        raise TypeError("No Twitter handle provided.")

# Bejing, China - None
# Tehran, Iran - Some
# 0,0 -Some
# Guatemala City - Some
# tokyo -
# jakarta
# buenos aires
# mexico city
# baku, azerbaijan
# trinidad, 
# berlin
# paris
# india
# moscow
# senegal
# turkey
# vietnam
# uzbekistan 
# caracas, venezuela
# south africa
# paraguay
# uruguay - lots
# canada - lots

geo_tagged = {'statuses': []}

# while len(geo_tagged) < 10: 
# print(twitter_data['statuses'][0]['geo'])
# print(twitter_data['statuses'][0]['user'].keys())
twitter_data = get_from_twitter(100)
for each in twitter_data['statuses']:
    if each['geo'] != None:
        geo_tagged['statuses'].append(each)
    elif each['place'] != None:
        geo_tagged['statuses'].append(each)
    elif each['coordinates'] != None:
        geo_tagged['statuses'].append(each)

print(len(geo_tagged['statuses']))



class Tweet(object):
    def __init__(self, tweet_dict):
        self.tweet_text = tweet_dict['text']
        self.date_created = tweet_dict['created_at']
        self.country = tweet_dict['place']['country']
        self.latitude = tweet_dict['place']['bounding_box']['coordinates'][0][0][0]
        self.longitude = tweet_dict['place']['bounding_box']['coordinates'][0][0][1]
        try:
            self.url = tweet_dict['entities']['urls'][0]['url']

        except: 
            self.url = ''



# instantiate class Tweet objects
tweets = []
for tweet in geo_tagged['statuses']:
    tweets.append(Tweet(tweet))
    # print(Tweet(tweet).url)



# create csv file
twitter_csv = open("twitter_results.csv", 'w', newline='')
twitter_writer = csv.writer(twitter_csv)
twitter_writer.writerow(['tweet_text','date_created', 'country', 'latitude', 'longitude', 'url'])
for tweet in tweets:
    twitter_writer.writerow([tweet.tweet_text, tweet.date_created, tweet.country, tweet.latitude, tweet.longitude, tweet.url])
twitter_csv.close()



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
