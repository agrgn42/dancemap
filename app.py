from flask import Flask, render_template, request, flash, jsonify
from forms import ContactForm
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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)



@app.route("/", methods=['GET', 'POST'])
def index():

	dance_sql.create_dance_db()
	dance_sql.create_flickr_table()
	dance_sql.create_twitter_table()
	dance_sql.create_youtube_table()
	dance_sql.create_countries_table()

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

		origin = repo.git.remote(name='origin')
		origin.push()

	except:
		pass


	# DANCE_GEOJSON = jsonify(fstring)
	return render_template("index.html", ACCESS_KEY=MAPBOX_ACCESS_KEY)





if __name__=="__main__":
    # model.init()
    app.run(debug=True)