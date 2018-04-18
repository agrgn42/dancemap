from flask import Flask, render_template, request, flash
from forms import ContactForm
from secrets import MAPBOX_ACCESS_KEY
 
app = Flask(__name__) 
 
app.secret_key = 'whiskii^honk#)ywooptonksh&'


@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)



@app.route("/")
def index():
    ## print the guestbook
    return render_template("index.html", ACCESS_KEY=MAPBOX_ACCESS_KEY)

if __name__=="__main__":
    # model.init()
    app.run(debug=True)