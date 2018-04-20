import json
import requests
import webbrowser
import csv
# from secret_data import FLICKR_KEY, NYT_KEY
from geotext import GeoText
import time

from secrets import FLICKR_KEY


CACHE_FNAME = 'flickr_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents_str = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents_str)
    cache_file.close()
except: 
    CACHE_DICTION = {}


# fcountries = "countries.json"
# fcountries_obj = open(fcountries, "r")
# fcountries_contents = fcountries_obj.read()
# COUNTRIES_DICT = json.loads(fcountries_contents)
# fcountries_obj.close()


#####################

def params_unique_combination(baseurl, params_d):
    alphabetized_keys = sorted(params_d.keys())
    results_keys=[]
    for k in alphabetized_keys:
        results_keys.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(results_keys)


def get_flickr_data(tag_search, num_photos=100):
    baseurl = "https://api.flickr.com/services/rest/"
    params_d = {}
    params_d['tags'] = tag_search
    params_d['per_page'] = num_photos
    params_d['api_key'] = FLICKR_KEY
    params_d['method'] = "flickr.photos.search"
    params_d['has_geo'] = True
    params_d['tag_mode'] = "all"
    params_d['format'] = "json"
    unique_identifier = params_unique_combination(baseurl, params_d)
    if unique_identifier in CACHE_DICTION:
        print('Getting cached Flickr data...')
        return CACHE_DICTION[unique_identifier]
    else:
        print('Making request for new Flickr data...')
        flickr_resp = requests.get(baseurl, params=params_d)
        flickr_text = flickr_resp.text
        if flickr_text == 'jsonFlickrApi({"stat":"fail","code":100,"message":"Invalid API Key (Key has invalid format)"})':
        	print("\nSorry, it appears the way you input your New York Times Article Search API key may be incorrect. Please try pasting it in again.\n")
        flickr_text_adjusted = flickr_text[14:-1]
        flickr_resp_python = json.loads(flickr_text_adjusted)
        CACHE_DICTION[unique_identifier] = flickr_resp_python
        entire_diction_json_string_to_cache = json.dumps(CACHE_DICTION)
        fwrite = open(CACHE_FNAME,'w')
        fwrite.write(entire_diction_json_string_to_cache)
        fwrite.close()
        return CACHE_DICTION[unique_identifier]



def get_flickr_photos_data(each_id):
    baseurl = "https://api.flickr.com/services/rest/"
    params_d = {}
    params_d['photo_id'] = each_id
    params_d['api_key'] = FLICKR_KEY
    params_d['method'] = "flickr.photos.getInfo"
    params_d['format'] = "json"
    unique_identifier = params_unique_combination(baseurl, params_d)
    if unique_identifier in CACHE_DICTION:
        print('Getting cached Flickr photo data...')
        return CACHE_DICTION[unique_identifier]
    else:
	    print('Making request for new Flickr photo data...')
	    flickr_resp = requests.get(baseurl, params=params_d)
	    flickr_text = flickr_resp.text
	    flickr_text_adjusted = flickr_text[14:-1]
	    flickr_resp_python = json.loads(flickr_text_adjusted)
	    CACHE_DICTION[unique_identifier] = flickr_resp_python
	    entire_diction_json_string_to_cache = json.dumps(CACHE_DICTION)
	    fwrite = open(CACHE_FNAME,'w')
	    fwrite.write(entire_diction_json_string_to_cache)
	    fwrite.close()
	    return CACHE_DICTION[unique_identifier]

class Photo(object):
    def __init__(self, photo_dict):
    	self.title = photo_dict["photo"]["title"]["_content"]
    	self.date_taken = photo_dict["photo"]["dates"]["taken"]
    	if "country" in photo_dict["photo"]["location"]:
    		self.country = photo_dict["photo"]["location"]["country"]["_content"]
    	else:
    		self.country = ""
    	self.latitude = photo_dict["photo"]["location"]["latitude"]
    	self.longitude = photo_dict["photo"]["location"]["longitude"]
    	for each in photo_dict["photo"]["urls"]["url"]:
    		self.url = each["_content"]

    def photo_geo_info(self):
    	return self.country, self.latitude, self.longitude

    def __str__(self):
        return "{}\n{}\n{}\n{}\n".format(self.title, self.date_taken, self.url, self.photo_geo_info())


def get_data(query = 'dance china'):


    photo_ids = []
    flickr_dance_request = get_flickr_data(tag_search = query)
    for diction in flickr_dance_request["photos"]["photo"]:
        photo_ids.append(diction["id"])

    for each_id in photo_ids:
    	flickr_photos_request = get_flickr_photos_data(each_id)

    return photo_ids

    
def make_photo_inst(CACHE_DICTION):
    
    photo_instances = []
    for k,v in CACHE_DICTION.items():
        try: 
            photo_instances.append(Photo(v))
        except:
            pass

    return photo_instances



if __name__ == "__main__":

    get_data()
    make_photo_inst(CACHE_DICTION)










