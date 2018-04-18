
from flask import Flask, render_template, request, redirect
import model
from secrets import EMAIL_USERNAME, EMAIL_PW
from flask_mail import Mail

# initialize mail app
mail = Mail(app)

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get(EMAIL_USERNAME)
MAIL_PASSWORD = os.environ.get(EMAIL_PW)

# administrator list
ADMINS = [EMAIL_USERNAME+'@gmail.com']




app = Flask(__name__)

@app.route("/")
def index():
    ## print the guestbook
    return render_template("index.html", entries=model.get_entries())

@app.route("/about")
def about():
    ## add a guestbook entry
    return render_template("addentry.html")


@app.route("/submit", methods=['POST'])
def submit():
    ## add a guestbook entry
    return render_template("submit.html")

@app.route("mailto:angela.schopke@gmail.com", methods=["POST"])
def postentry():
    name = request.form["dancename"]
    country1 = request.form["country1"]
    state1 = request.form["state1"]
    city1 = request.form["city1"]
    address = request.form["address"]
    photos = request.form["photos"]
    photocredit = request.form["photocredit"]
    website = request.form["website"]
    country2 = request.form["country2"]
    state2 = request.form["state2"]
    city2 = request.form["city2"]
    gender = request.form["gender"]
    year = request.form["year"]
    email = request.form["email"]
    model.add_entry(name, message)
    return redirect("/")    # redirects to a given page

if __name__=="__main__":
    model.init()
    app.run(debug=True)




# with gunicorn:
# gunicorn app:app - looks inside object called app to run app.py file
# heroku communicates with git
# Create a `requirements.txt` file.
# Create a `runtime.txt` file. This will tell Heroku what version of Python to run.
# run `python --version` to find out what version you’re running
# write a single line into your `runtime.txt` file that looks like this (using your python version): python-3.6.4
# Create a `Procfile`. This is a file that will tell Heroku how to run your app. Again, just one line: web: gunicorn app:app --log-file=-
# Create a git repository in your project directory
# First, create a .gitignore and put in it: 
#   venv 
#   __pycache__
# git init 
# git add .
# git commit -m "first commit"

# heroku login
# heroku create

# remote -v
# heroku  https://git.heroku.com/tranquil-ravine-49028.git (fetch)
# heroku  https://git.heroku.com/tranquil-ravine-49028.git (push)
# git push heroku master

# git remote add origin https://github.com/agrgn42/herokutest.git

# now you can either "git push origin master" to update code, and then "git push heroku master" to deploy to the world





