from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.fields.core import BooleanField, SelectField, RadioField
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from datetime import datetime

class SchedulePickupForm(FlaskForm):
    location = SelectField("Location", choices=["Beaver Falls", "Chippewa", "Grove City"])
    pickup = SelectField("Choose Pickup", choices=["In Store", "Drive Through"])
    dayPicker = SelectField("Day", choices=["Today", "Tomorrow", "Next Day"])
    timePicker = TimeField("", format='%H:%M', default=datetime.now())
    goBackBut = SubmitField("Back")
    continueBut = SubmitField("Continue")

