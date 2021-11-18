from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.validators import InputRequired, equal_to

class ScheduleForm(FlaskForm):
    #TODO fill in