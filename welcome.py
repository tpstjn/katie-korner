#############################
# Welcome to Katie's Korner!
# Includes login and register
#############################

#########
# Imports
#########
import os, sys
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

from security.hashing import UpdatedHasher
from forms.login_forms import LoginForm, RegisterForm

#####################
# Basic Configuration
#####################

# Identify necessary files
dbfile = os.path.join(script_dir, "katie's_korner.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")

# open and read the contents of the pepper file into your pepper key
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()

# create a new instance of UpdatedHasher using that pepper key
pwd_hasher = UpdatedHasher(pepper_key)

# Configure Flask App
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'folgawoogaimogawomp'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get database object
db = SQLAlchemy(app)

# Prepare and connect LoginManager
app.login_manager = LoginManager()
app.login_manager.login_view = 'login'
# Customers
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

##########
# Database
##########
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary)
    user_role = db.Column(db.Unicode, nullable=False) # differentiate between different types of users

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)
    
    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)

class IceCreamFlavors(db.Model):
    __tablename__ = 'IceCreamFlavors'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Unicode, nullable=False)
    isRegularFlavor = db.Column(db.Boolean, nullable=False)
    isSherbet = db.Column(db.Boolean, nullable=False)
    hasSugar = db.Column(db.Boolean, nullable=False)

# db.drop_all()
db.create_all() # this is only needed if the database doesn't already exist

# banana = IceCreamFlavors(flavor="Banana", isRegularFlavor=True, isSherbet=False, hasSugar=True)
# blackCherry = IceCreamFlavors(flavor="Black Cherry", isRegularFlavor=True, isSherbet=False, hasSugar=True)
# cottonCandy = IceCreamFlavors(flavor="Cotton Candy", isRegularFlavor=True, isSherbet=False, hasSugar=True)
# bubbleGum = IceCreamFlavors(flavor="Bubble Gum", isRegularFlavor=True, isSherbet=False, hasSugar=True)
# chocolate = IceCreamFlavors(flavor="Chocolate", isRegularFlavor=True, isSherbet=False, hasSugar=True)

# blueBoy = IceCreamFlavors(flavor="Blue Boy", isRegularFlavor=False, isSherbet=True, hasSugar=True)
# orange = IceCreamFlavors(flavor="Orange", isRegularFlavor=False, isSherbet=True, hasSugar=True)
# redRasp = IceCreamFlavors(flavor="Red Raspberry", isRegularFlavor=False, isSherbet=True, hasSugar=True)

# butterPecan = IceCreamFlavors(flavor="Cutter Pecan", isRegularFlavor=False, isSherbet=False, hasSugar=False)
# ripple = IceCreamFlavors(flavor="Fudge Ripple", isRegularFlavor=False, isSherbet=False, hasSugar=False)
# vanilla = IceCreamFlavors(flavor="Vanilla", isRegularFlavor=False, isSherbet=False, hasSugar=False)

# db.session.add(banana)
# db.session.add(blackCherry)
# db.session.add(cottonCandy)
# db.session.add(bubbleGum)
# db.session.add(chocolate)
# db.session.add(blueBoy)
# db.session.add(orange)
# db.session.add(redRasp)
# db.session.add(butterPecan)
# db.session.add(ripple)
# db.session.add(vanilla)

# db.session.commit()

################
# Route Handlers
################

###########
# Home Page
###########
@app.route("/")
def index():
    # Make sure user was loaded properly (just in case)
    if current_user.is_authenticated:
        return render_template('home.j2', current_user=current_user)
    else:
        return render_template('home.j2')

#######
# Login
#######    
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.j2', form=form)

    if request.method == 'POST':
        if form.validate():

            # try to get the user associated with this email address
            # check if user is a Customer
            user = User.query.filter_by(email=form.email.data).first()
            # if user exists and password matches...
            if user is not None and user.verify_password(form.password.data):
                # log this user in through the login_manager
                login_user(user, remember=form.rememberMe.data)
                # redirect the user to the page they wanted or the home page
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('index')
                return redirect(next)
            else:
                flash("Wrong username or password")
                return redirect(url_for('login'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('login'))

###################
# Register Customer
###################
@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.j2', form=form)
    if request.method == 'POST':
        if form.validate():
            # Check if email & pwd are in DB
            user = User.query.filter_by(email=form.email.data).first()
            # if the email address is free, create a new user and send to login
            if user is None:
                user = User(email=form.email.data, password=form.password.data, user_role="Customer")
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else: # if user already exists
                # flash warning message and redirect
                flash('There is already an account with that email address')
                return redirect(url_for('register'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('register'))

###################
# Register Employee
###################
@app.route("/register-employee/", methods=["GET", "POST"])
def register_employee():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.j2', form=form)
    if request.method == 'POST':
        if form.validate():
            # Check if email & pwd are in DB
            user = User.query.filter_by(email=form.email.data).first()
            # if the email address is free, create a new user and send to login
            if user is None:
                user = User(email=form.email.data, password=form.password.data, user_role="Employee")
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else: # if user already exists
                # flash warning message and redirect
                flash('There is already an account with that email address')
                return redirect(url_for('register_employee'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('register_employee'))

########
# Logout
########
@app.get('/logout/')
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

#########
# Flavors
#########
@app.get('/flavors/')
def flavors():
    # flavorList = IceCreamFlavors.query.all()
    # flavorMessage = ""
    # for flavor in flavorList:
    #     flavorMessage += f"{flavor.flavor} : {flavor.isRegularFlavor} : {flavor.isSherbet} : {flavor.hasSugar}\n"
    # flash(flavorMessage)
    if current_user.is_authenticated:
        return render_template('flavors.j2', current_user=current_user, flavorList=IceCreamFlavors.query.all())
    else:
        return render_template('flavors.j2', flavorList=IceCreamFlavors.query.all())