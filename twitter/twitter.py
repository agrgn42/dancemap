# from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
import json
import sys
import requests
import nltk
from nltk.corpus import stopwords
import csv

from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_KEY
access_secret = ACCESS_SECRET

#Code for OAuth starts
oauth = OAuth1Session(consumer_key, consumer_secret, access_token, access_secret)
#Code for OAuth ends


CACHE_FNAME = 'twitter_cache.json'
COORDS_FNAME = 'country-capitals.csv'

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents_str = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents_str)
	cache_file.close()
except:
    CACHE_DICTION = {}


###########################################


# generate unique identifier for each api request
def params_unique_combination(baseurl, params_d):
	alphabetized_keys = sorted(params_d.keys())
	results_keys=[]
	for k in alphabetized_keys:
		results_keys.append("{}-{}".format(k, params_d[k]))
	return baseurl + "_".join(results_keys)


def get_from_twitter(coords, count=25):
    try:
        baseurl = "https://api.twitter.com/1.1/search/tweets.json"
        params_d = {}
        params_d["q"] = "dance"
        params_d["result_type"] = "recent"
        params_d["geocode"] = coords
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



class Tweet(object):
    def __init__(self, tweet_dict):
        self.id_str = tweet_dict['id_str']
        self.tweet_text = tweet_dict['text']
        self.date_created = tweet_dict['created_at']
        self.country = tweet_dict['place']['country']
        self.latitude = tweet_dict['place']['bounding_box']['coordinates'][0][0][0]
        self.longitude = tweet_dict['place']['bounding_box']['coordinates'][0][0][1]
        try:
            self.url = tweet_dict['entities']['urls'][0]['url']

        except: 
            self.url = ''



def get_geotagged(CACHE_DICTION):


    geo_tagged = {'statuses': []}
    
    for k,v in CACHE_DICTION.items():

        for geoitem in v['statuses']:

            if geoitem['geo'] != None:
                geo_tagged['statuses'].append(geoitem)
            elif geoitem['place'] != None:
                geo_tagged['statuses'].append(geoitem)
            elif geoitem['coordinates'] != None:
                geo_tagged['statuses'].append(geoitem)

    return geo_tagged


def make_tweet_inst(geo_tagged):

    # instantiate class Tweet objects
    tweets = []
    for tweet in geo_tagged['statuses']:
        try:
            tweets.append(Tweet(tweet))
        except:
            pass

    return tweets



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()


    with open(COORDS_FNAME) as infile:
        reader = csv.reader(infile) # comma is default delimiter
        
        while len(CACHE_DICTION.items()) < 100:
            for row in reader:
                if row[0] != 'CountryName':
                    search_coords = str(row[2]) + ',' + str(row[3]) + ',1000km'
        
                    twitter_data = get_from_twitter(search_coords, 100)



