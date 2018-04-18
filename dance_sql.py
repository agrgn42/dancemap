import csv
import json
from sqlite3 import Error
import sqlite3 as sqlite

import pkgutil
import encodings
import os


DB_NAME = 'dance.db'
COUNTRIESJSON = 'countries.json'

countries_file = open('countries.json', 'r')
countries_contents = countries_file.read()
countries_dict = json.loads(countries_contents)
countries_file.close()
  

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
        Url TEXT
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
    


def create_flickr_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO Flickr
        VALUES (NULL,?,?,?,?,?,?,NULL)
        '''
    with open('flickr/flickr_results.csv', 'r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            params = (row[0], row[1], row[2], row[3], row[4], row[5])
            cur.execute(insert, params)

    conn.commit()
    conn.close()


def create_twitter_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO Twitter
        VALUES (NULL,?,?,?,?,?,?,NULL)
        '''
    with open('twitter/twitter_results/twitter_results_master.csv', 'r', encoding='ISO-8859-1') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            params = (row[0], row[1], row[2], row[3], row[4], row[5])
            cur.execute(insert, params)

    conn.commit()
    conn.close()

def create_youtube_table():

    conn = sqlite.connect(DB_NAME)
    cur = conn.cursor() 

    insert = '''
        INSERT INTO YouTube
        VALUES (NULL,?,?,?,?,?,?)
        '''
    with open('youtube/youtube_results.csv', 'r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            params = (row[0], row[1], row[2], row[3], row[4], row[5])
            cur.execute(insert, params)

    conn.commit()
    conn.close()



def create_countries_table():

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
        WHERE Twitter.Country = Countries.EnglishName OR Countries.EnglishName LIKE '%' || Twitter.Country || '%');
        '''
    cur.execute(update)


    conn.commit()
    conn.close()




if __name__ == "__main__":
    create_dance_db()
    create_flickr_table()
    create_twitter_table()
    create_youtube_table()
    create_countries_table()

    

