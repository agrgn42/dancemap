import unittest
from dance_sql import *
from flickr.flickr import *
from twitter.twitter import *
from youtube.youtube import *
import sqlite3 as sqlite
import dance_sql


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


class TestDatabase(unittest.TestCase):

    def test_flickr_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = 'SELECT Country FROM Flickr'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('United States',), result_list)
        self.assertEqual(len(result_list), 123)

        conn.close()

    def test_youtube_table(self):

        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        countries_list = dance_sql.update_youtube_table()
        self.assertIn('South Africa', countries_list)
        self.assertIn('Poland', countries_list)

        conn.close()


    def test_country_table(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = '''
            SELECT EnglishName
            FROM Countries
            WHERE Region="Oceania"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Australia',), result_list)
        self.assertEqual(len(result_list), 27)

        sql = '''
            SELECT COUNT(*)
            FROM Countries
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 250)

        conn.close()

    def test_joins(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        sql = '''
            SELECT Alpha2
            FROM Twitter
                JOIN Countries
                ON Twitter.CountryId=Countries.Id
            WHERE TweetText="#SalsaBogo #Dance una academia de #baile que alquila 3 ambientes de diferentes tamaños y que se puede aprovechar pa… https://t.co/dddE3VbZOv"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('CO',), result_list)

        conn.close()

    def reset_tables(self):
        conn = sqlite.connect(DB_NAME)
        cur = conn.cursor()

        dance_sql.create_dance_db()
        dance_sql.update_flickr_table()
        dance_sql.update_twitter_table()
        dance_sql.update_youtube_table()
        dance_sql.update_countries_table()

        conn.close()

class TestYouTube(unittest.TestCase):

    def test_youtube_search(self):
        videos = youtube.youtube.make_video_inst(youtube_dict)
        self.assertEqual(len(videos), 100)
        self.assertEqual(videos[0].title, 'Romane Gila 2018 - LATINO DANCE')

class TestFlickr(unittest.TestCase):

    def test_flickr_search(self):
        photos = flickr.flickr.make_photo_inst(flickr_dict)
        self.assertEqual(len(photos), 123)
        self.assertEqual(photos[0].latitude, '40.740038')
        self.assertEqual(photos[0].longitude, '-74.009141')


class TestTwitter(unittest.TestCase):

    def test_twitter_search(self):
        tweets = twitter.twitter.make_tweet_inst(twitter.twitter.get_geotagged(twitter_dict))
        self.assertEqual(len(tweets), 299)
        self.assertEqual(tweets[0].country, 'United States')


unittest.main()