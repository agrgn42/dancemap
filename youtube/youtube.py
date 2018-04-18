from secrets import YOUTUBE_KEY
import json
import csv


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from secrets import YOUTUBE_KEY



YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

CACHE_FNAME = 'youtube_cache.json'

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


def youtube_search(q, location, location_radius, max_results):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=YOUTUBE_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query terms

	baseurl = "https://www.googleapis.com/youtube/v3"
	params_d = {}
	params_d['q']=q
	params_d['type']='video'
	params_d['order']='date'
	params_d['safeSearch']='moderate'
	params_d['location']=location
	params_d['location_radius']=location_radius
	params_d['part']='id,snippet'
	params_d['maxResults']=max_results
	unique_identifier = params_unique_combination(baseurl, params_d)
	if unique_identifier in CACHE_DICTION:
		print('Getting cached YouTube data...')
		return CACHE_DICTION[unique_identifier]
	else:
		print('Making request for new YouTube data...')
		youtube_response = youtube.search().list(
			q=q,
			type='video',
			order='date',
			safeSearch='moderate',
			location=location,
			locationRadius=location_radius,
			part='id,snippet',
			maxResults=max_results
		).execute()
		# print(type(youtube_response))
		CACHE_DICTION[unique_identifier] = youtube_response
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fwrite = open(CACHE_FNAME,'w')
		fwrite.write(dumped_json_cache)
		fwrite.close()
		return CACHE_DICTION[unique_identifier]


def video_location(search_response):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=YOUTUBE_KEY)

	baseurl = "https://www.googleapis.com/youtube/v3"
	params_d = {}
	params_d['id']=video_ids
	params_d['part']='snippet, recordingDetails'
	unique_identifier = params_unique_combination(baseurl, params_d)
	if unique_identifier in CACHE_DICTION:
		print('Getting cached video data...')
		return CACHE_DICTION[unique_identifier]
	else:
		print('Making request for new video data...')
		video_response = youtube.videos().list(
			id=video_ids,
			part='snippet, recordingDetails'
		).execute()
		CACHE_DICTION[unique_identifier] = video_response
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fwrite = open(CACHE_FNAME,'w')
		fwrite.write(dumped_json_cache)
		fwrite.close()
		return CACHE_DICTION[unique_identifier]


def display_locations(video_response):

	videos=[]

	for video_result in video_response.get('items', []):
		print(video_result)
		videos.append('%s, (%s,%s)' % (video_result['snippet']['title'],
			video_result['recordingDetails']['location']['latitude'],
			video_result['recordingDetails']['location']['longitude']))

	print('Videos:\n', '\n'.join(videos), '\n')

	return videos


class Video(object):
    def __init__(self, video_dict):
        self.title = video_dict['snippet']['title']
        self.date_created = video_dict['snippet']['publishedAt']
        try:
        	self.place_name = video_dict['recordingDetails']['locationDescription']
        except:
        	self.place_name = ''
        self.latitude = video_dict['recordingDetails']['location']['latitude']
        self.longitude = video_dict['recordingDetails']['location']['longitude']
        self.url = 'https://www.youtube.com/watch?v=' + video_dict['id']
        self.thumbnail = video_dict['snippet']['thumbnails']['default']['url']



if __name__ == '__main__':
	search_response = youtube_search('dance', '35.6892,51.3890', '1000km', '50')
	
	search_videos = []
	for search_result in search_response.get('items', []):
		search_videos.append(search_result['id']['videoId'])

	video_ids = ','.join(search_videos)
	responses = video_location(video_ids)


	videos = []

	# instantiate class Video objects
	for video in responses['items']:
		print(video)
		videos.append(Video(video))
		

	# create csv file
	youtube_csv = open("youtube_results.csv", 'w', newline='')
	youtube_writer = csv.writer(youtube_csv)
	youtube_writer.writerow(['title','date_created', 'place_name', 'latitude', 'longitude', 'url'])
	for video in videos:
	    youtube_writer.writerow([video.title, video.date_created, video.place_name, video.latitude, video.longitude, video.url])
	youtube_csv.close()














