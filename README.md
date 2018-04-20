# dancemap

# Program Overview
This program opens an HTML page using Python's Flask and weebbrowser modules. 

This web page features a d3.js world map visualization constructed by Angela Schopke.
The program populates this map visualization with data retrieved via Flickr, Twitter, and YouTube Data APIs (details below), stored in an SQL database, and called by this program's Flask application. A php script allows this map-to-database connection to function. 

A map viewer can search for locations of interest from the mapping interface in order to filter the results provided according to the desired location. This search functionality contributes multiple data views via the map's zoom feature on search.


# Data Sources

The program retrieves data from each of the following data source. In order to use each of these date sources, the program user will need to set up developer accounts with each resource, and include relevant user-specific keys in secrets.py files. More details on which keys are necessary are discussed in greater detail below. Please ensure that your .gitignore file includes 'secrets.py' in order to avoid publishing your user keys publically.

Flickr API
https://www.flickr.com/services/api/
Information to include in a secrets.py file storied in 'flickr' directory:
FLICKR_KEY = 'your_flickr_key

Twitter API
https://developer.twitter.com/en/docs/tweets/search/overview
Information to include in a secrets.py file file storied in 'twitter' directory:
CONSUMER_KEY = 'your_twitter_consumer_key'
CONSUMER_SECRET = 'your_twitter_consumer_secret'
ACCESS_KEY = 'your_twitter_access_key'
ACCESS_SECRET = 'your_twitter_access_secret'

YouTube Data APIv3 (query for "dance")
https://developers.google.com/youtube/v3/
Information to include in a secrets.py file storied in 'youtube' directory:
YOUTUBE_KEY = 'your_youtube_key'

MapBox GL JS API:
https://www.mapbox.com/mapbox-gl-js/api/
Information to include in a secrets.py file storied in main directory:
MAPBOX_ACCESS_KEY = 'your_mapbox_key'


# Running the Program

VIRTUAL ENVIRONMENT SETUP:

From terminal (Mac OS), navigate to the 'dancemap' directory. To create a virtual environment, run the command...

    virtualenv daenv

To install required program dependencies, run the command...

    pip install -r requirements.txt


DATA UPDATES:

Depending the desired data source to update from, run any of 'twitter.py', 'flickr.py', or 'youtube.py' as needed using the following input parameters.

'youtube.py'
Run this file to update YouTube data.
In-file required input parameters:
  
  'youtube_search' function - 
  
      query = 'keyword_you_want_to_search_for_videos_of'
        default = 'dance'
      location = 'lat,lng'
        default = '-29.3166,27.4833'
      location_radius = 'number_of_kilmoters_from_location_to_search"
        deault = '1000km'
      max_results = maximum_number_of_results_returned
        default = 50 # this must be an integer less than or equal to 50
 
 
'flickr.py'
Run this file to update Flickr data.
In-file required input parameters:
  
  'get_data' function - 
  
      query = 'keyword_you_want_to_search_for_videos_of'
        default = 'dance china'
        NOTE - searching for 'dance' plus a country, province, or city keyword returns a broader range of results than a 
        search for only 'dance'


'twitter.py'
Run this file to update Twitter data.
In-file required input parameters:
  
  'get_from_twitter' function - 
  
        coords = Given the low volume of geo-tagged Tweets, this function automatically calls multiple locations around the                    world until at least 100 geo-tagged results for the given query term.
        query = 'keyword_you_want_to_search_for_videos_of'
          default = 'dance'
        count = maximum_number_of_results_returned
          default = 100


DISPLAYING DATA IN MAP:

From terminal (Mac OS) with your virtual environment activated in the 'dancemap' directory, run the command...

    python app.py

This command will automatically build and update your database, run the php script necessary to render the datapoints in .geojson format necessary to populate the map, push these files to the master branch of the GitHub repository you have initialized your 'dancemap' directory with in order that the map's javascript can access the file's contents via necessary URL, and render the map.

NOTE that the map may take several minutes to populate with new data given that it relies on web-hosted geojson data, which may take GitHub some time to get up and running. 

To view the map, open your web browser and enter the following URL...

  http://localhost:5000


CHOOSING DIFFERENT MAP VIEWS:

To select different map views, enter a location-based search term in the search bar included with the map. The search function will provide suggestions to autocomplete your location-based search term in order that your search is compliant with necessary geocoding retrieval processes. Press 'enter' on your keyboard to execute the search. You will see the map zoom in to view the specified area.


  
        
    





