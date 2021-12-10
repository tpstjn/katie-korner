from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField
from wtforms.fields.core import BooleanField, IntegerField, SelectField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange, Optional

class RateFlavorForm(FlaskForm):
    rating = IntegerField("Rating: ", 
        validators=[InputRequired(), NumberRange(min=0, max=5)])
    comment = StringField("Comment: ", 
        validators=[Optional(), Length(min=1,max=512)])
    submit = SubmitField("Submit")