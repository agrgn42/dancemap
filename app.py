from flask import Flask, render_template, request, flash, jsonify
from forms import ContactForm
from secrets import MAPBOX_ACCESS_KEY
import json
import dance_sql
import os


 
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
	## return the geo data and mapbox key to the map page
	# fname = 'dance.geojson'
	# fopen = open(fname, 'r')
	# DANCE_GEOJSON = fopen.read()
	# fopen.close()

	dance_sql.create_dance_db()
	dance_sql.create_flickr_table()
	dance_sql.create_twitter_table()
	dance_sql.create_youtube_table()

	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/flickr_mapbox.php")
	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/twitter_mapbox.php")
	os.system("php /Users/angelaschopke/Documents/SI507/final_proj/dancemap/youtube_mapbox.php")

	# DANCE_GEOJSON = jsonify(fstring)
	return render_template("index.html", ACCESS_KEY=MAPBOX_ACCESS_KEY)





if __name__=="__main__":
    # model.init()
    app.run(debug=True)