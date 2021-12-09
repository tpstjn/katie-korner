from flask_wtf import FlaskForm
from flask_wtf.form import SUBMIT_METHODS
from wtforms.fields import PasswordField, SubmitField
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", 
        validators=[EqualTo('password')])
    submit = SubmitField("Register")

class RegisterEmployeeForm(FlaskForm):
    firstName = TextField("First Name", 
        validators=[InputRequired(message="Required")], 
        render_kw={"placeholder": "John"})
    lastName = TextField("Last Name", 
        validators=[InputRequired(message="Required")], 
        render_kw={"placeholder": "Smith"})
    role = SelectField("Role", 
        validators=[InputRequired(message="Required")],
        choices=[],
        render_kw={"placeholder": "Role"})
    email = EmailField("Email", 
        validators=[InputRequired(message="Required"), 
                    Email(message="Must be a valid email address")], 
        render_kw={"placeholder": "name@example.com"})
    password = PasswordField("Password", 
        validators=[InputRequired(message="Required"), 
                    Length(min=8, max=256, message="Password must be between 8 and 256 characters")],
        render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Confirm Password", 
        validators=[EqualTo('password', message="Passwords must match")],
        render_kw={"placeholder": "Confirm Password"})
    submitRegister = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    rememberMe = BooleanField("Remember me")
    submit = SubmitField("Login")

class EditEmployeeForm(FlaskForm):
    name = TextField("Name",
        render_kw={"disabled": "True"})
    role = SelectField("Role", 
        validators=[InputRequired(message="Required")],
        choices=[],
        render_kw={"placeholder": "Role"})
    submitEdit = SubmitField("Make Changes")