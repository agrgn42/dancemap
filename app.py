from flask import Flask, render_template, request, flash, jsonify
from secrets import MAPBOX_ACCESS_KEY
import json
import os
import git
import sys 

import dance_sql
sys.path.append('youtube/')
import youtube
sys.path.append('twitter/')
import twitter
sys.path.append('flickr/')
import flickr

 
app = Flask(__name__) 
 
app.secret_key = 'whiskii^honk#)ywooptonksh&'


@app.route("/", methods=['GET', 'POST'])
def index():

	dance_sql.create_dance_db()
	dance_sql.update_flickr_table()
	dance_sql.update_twitter_table()
	dance_sql.update_youtube_table()
	dance_sql.update_countries_table()

	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/flickr_mapbox.php")
	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/twitter_mapbox.php")
	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/youtube_mapbox.php")

	try:
		local_dir = '/Users/angelaschopke/Documents/SI507/final_proj/dancemap'
		repo = git.Repo(local_dir)

		repo.git.add("flickr.geojson")
		repo.git.add("twitter.geojson")
		repo.git.add("youtube.geojson")
		
		repo.git.commit("-m 'new geo data'")

		repo.remotes.origin.push()

	except:
		pass

	return render_template("index.html", ACCESS_KEY=MAPBOX_ACCESS_KEY)





if __name__=="__main__":

    app.run(debug=True)
    