from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.fields.core import BooleanField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange
from datetime import datetime

from wtforms.widgets.core import Input

class SchedulePickupForm(FlaskForm):
    location = SelectField("Location", choices=["Beaver Falls", "Chippewa", "Grove City"])
    pickup = SelectField("Choose Pickup", choices=["In Store", "Drive Through"])
    dayPicker = SelectField("Day", choices=["Today", "Tomorrow", "Next Day"])
    timePicker = TimeField("", format='%H:%M', default=datetime.now())
    goBackBut = SubmitField("Back")
    continueBut = SubmitField("Continue")

class OrderPint(FlaskForm):
    flavor = SelectField("Flavor", 
            choices=[],
            validators=[InputRequired()])
    quantity = IntegerField("Quantity", 
            validators=[NumberRange(min=1, max=20),
            InputRequired()])
    submitOrderPint = SubmitField("Add to Checkout")

class OrderMilkshake(FlaskForm):
    flavor = SelectField("Flavor",
            choices=[],
            validators=[InputRequired()])
    quantity = IntegerField("Quantity", 
            validators=[NumberRange(min=1, max=20),
            InputRequired()])
    addWhippedCream = BooleanField("Whipped Cream?")
    addCherry = BooleanField("Cherry?")
    submitOrderMilkshake = SubmitField("Add to Checkout")

class OrderCone(FlaskForm):
    flavor = SelectField("Flavor",
            choices=[],
            validators=[InputRequired()])
    quantity = IntegerField("Quantity", 
            validators=[NumberRange(min=1, max=20),
            InputRequired()])
    coneType = SelectField("Cone Type",
            choices=["Waffle", "Cake", "Sugar"],
            validators=[InputRequired()])
    numOfScoops = IntegerField("Number of Scoops",
            validators=[NumberRange(min=1, max=3),
            InputRequired()])
    submitOrderCone = SubmitField("Add to Checkout")

class OrderSundae(FlaskForm):
    specialItem = RadioField("Specialties",
            choices=[""])