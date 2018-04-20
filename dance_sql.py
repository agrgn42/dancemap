import csv
import json
from sqlite3 import Error
import sqlite3 as sqlite
from geopy.geocoders import Nominatim
import requests

import pkgutil
import encodings
import os
import sys

import flickr.flickr
import twitter.twitter
from twitter.twitter import CACHE_DICTION as tweet_data
import youtube.youtube

DB_NAME = 'dance.db'
COUNTRIESJSON = 'countries.json'
FLICKRJSON = 'flickr/flickr_cache.json'
TWITTERJSON = 'twitter/twitter_cache.json'
YOUTUBEJSON = 'youtube/youtube_cache.json'

countries_file = open(COUNTRIESJSON, 'r')
countries_contents = countries_file.read()
countries_dict = json.loads(countries_contents)
countries_file.close()

flickr_file = open(FLICKRJSON, 'r')
flickr_contents = flickr_file.read()
flickr_dict = json.loads(flickr_contents)
flickr_file.close()

twitter_file = open(TWITTERJSON, 'r')
twitter_contents = twitter_file.read()
twitter_dict = json.loads(twitter_contents)
twitter_file.close()

youtube_file = open(YOUTUBEJSON, 'r')
youtube_contents = youtube_file.read()
youtube_dict = json.loads(youtube_contents)
youtube_file.close()



def create_dance_db():

    # connecting to db
    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor()

    # dropping existing tables to start fresh
    statement = '''
        DROP TABLE IF EXISTS 'Twitter';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Flickr';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'YouTube';
    '''
    cur.execute(statement)


    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)
    conn.commit()


    # creating tables
    statement = '''
    CREATE TABLE Flickr (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        DateCreated DATE,
        Country TEXT,
        Latitude REAL,
        Longitude REAL,
        Url TEXT,
        CountryId INTEGER
    );
    '''
    cur.execute(statement)


    statement = '''
    CREATE TABLE Twitter (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        TweetText TEXT,
        DateCreated DATE,
        Country TEXT,
        Latitude REAL,
        Longitude REAL,
        Url TEXT,
        CountryId INTEGER
    );
    '''
    cur.execute(statement)

    statement = '''
    CREATE TABLE YouTube (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        DateCreated DATE,
        PlaceName TEXT,
        Latitude REAL,
        Longitude REAL,
        Url TEXT,
        Country TEXT,
        CountryId INTEGER
    );
    '''
    cur.execute(statement)


    statement = '''
    CREATE TABLE Countries (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Alpha2 TEXT, --2 letter country code
        Alpha3 TEXT, --3 letter country code
        EnglishName TEXT, --English name for country
        Region TEXT, --Broad region where country is located.
        Subregion TEXT, --More specific subregion where country is located.
        Population INTEGER, --Country’s population
        Area REAL --Country’s area in km2
    );
    '''
    cur.execute(statement)


    conn.commit()
    cur.close()
    conn.close()
    


def update_flickr_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO Flickr
        VALUES (NULL,?,?,?,?,?,?,NULL)
        '''

    for photo in flickr.flickr.make_photo_inst(flickr_dict):

        params = (photo.title, photo.date_taken, photo.country, photo.latitude, photo.longitude, photo.url)
        cur.execute(insert, params)
   
    conn.commit()
    conn.close()


def update_twitter_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO Twitter
        VALUES (NULL,?,?,?,?,?,?,NULL)
        '''


    for tweet in twitter.twitter.make_tweet_inst(twitter.twitter.get_geotagged(twitter_dict)):
        params = (tweet.tweet_text, tweet.date_created, tweet.country, tweet.latitude, tweet.longitude, 'https://www.twitter.com/anyuser/status' + tweet.id_str)
        cur.execute(insert, params)


    conn.commit()
    conn.close()

def update_youtube_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO YouTube
        VALUES (NULL,?,?,?,?,?,?,?,NULL)
        '''

    countries_list = []
    for video in youtube.youtube.make_video_inst(youtube_dict):
        result = {}
        url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={}'
        request = url.format(str(video.latitude)+','+str(video.longitude))
        data = requests.get(request).json()
        country = None
        if len(data['results']) > 0:
            result = data['results'][0]
        if (not result is None) and ('address_components' in result):
            for component in result['address_components']:
                if 'country' in component['types']:
                    country = component['long_name']
                    countries_list.append(country)
                else:
                    country = None
        params = (video.title, video.date_created, video.place_name, video.latitude, video.longitude, video.url, country)
        cur.execute(insert, params)

    conn.commit()
    conn.close()

    return countries_list


def update_countries_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
            INSERT INTO Countries
            VALUES (NULL,?,?,?,?,?,?,?)
            '''

    for country in countries_dict:
        params = (country['alpha2Code'],
            country['alpha3Code'],
            country['name'],
            country['region'],
            country['subregion'],
            country['population'],
            country['area'])
        cur.execute(insert, params)


    update = '''
        UPDATE Flickr
        SET CountryId = (
        SELECT Countries.Id
        FROM Countries
        WHERE Flickr.Country=Countries.EnglishName OR Countries.EnglishName LIKE '%' || Flickr.Country || '%');
        '''
    cur.execute(update)


    update = '''
        UPDATE Twitter
        SET CountryId = (
        SELECT Countries.Id
        FROM Countries
        WHERE Twitter.Country = Countries.EnglishName 
        OR Countries.EnglishName LIKE '%' || Twitter.Country || '%' 
        OR Twitter.Country LIKE '%Iran%' AND  Countries.EnglishName LIKE '%Iran%' 
        OR Twitter.Country LIKE '%Korea%' AND Countries.EnglishName LIKE '%Korea%'
        OR Twitter.Country LIKE '%Croatia%' AND Countries.EnglishName LIKE '%Croatia%'
        OR Twitter.Country LIKE '%Philippines%' AND Countries.EnglishName LIKE '%Philippines%');
        '''
    cur.execute(update)

    update = '''
        UPDATE YouTube
        SET CountryId = (
        SELECT Countries.Id
        FROM Countries
        WHERE YouTube.Country = Countries.EnglishName OR Countries.EnglishName LIKE '%' || YouTube.Country || '%');
        '''
    cur.execute(update)

    conn.commit()
    conn.close()




if __name__ == "__main__":
    create_dance_db()
    update_flickr_table()
    update_twitter_table()
    update_youtube_table()
    update_countries_table()

    

