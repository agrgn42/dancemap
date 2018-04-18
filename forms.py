from flask_wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, SubmitField, validators, ValidationError
 
class ContactForm(Form):
  name = TextField("Name", [validators.Required()])
  email = TextField("Email", [validators.Required(), validators.Email()])
  subject = TextField("Subject", [validators.Required()])
  message = TextAreaField("Message", [validators.Required()])
  submit = SubmitField("Send")