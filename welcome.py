#############################
# Welcome to Katie's Korner!
# Includes login and register
#############################

# region Import/Basic Init

#########
# Imports
#########
from forms.login_forms import LoginForm, RegisterForm
from security.hashing import UpdatedHasher
import os
import sys
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login.utils import fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, AnonymousUserMixin, login_manager, login_required
from flask_login import login_user, logout_user, current_user

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

# endregion

# region Basic Config

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
app.config['KATIES_ADMIN'] = 'tpstjn@gmail.com'

# Get database object
db = SQLAlchemy(app)

# Prepare and connect LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# endregion

# region Database

##########
# Database
##########

# region Permissions

# Enumerates permissions allowed to various users
class Permission:
    ORDER = 1
    ADD_FLAVOR = 2
    ADMIN = 4

# endregion

# region Role

# Various roles users can have (Customer, Employee, Admin)
class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, permission):
        return (self.permissions & permission == permission)

    # For testing purposes
    @staticmethod
    def insert_roles():
        roles = {
            'Customer': [Permission.ORDER],
            'Employee': [Permission.ORDER, Permission.ADD_FLAVOR],
            'Administrator': [Permission.ORDER, Permission.ADD_FLAVOR, Permission.ADMIN]
        }
        default_role = 'Customer'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
# endregion

# region User

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary)
    # differentiate between different types of users
    user_role = db.Column(db.Integer, db.ForeignKey('Roles.id'))

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

    # If app defines user as admin, make admin
    # Otherwise, set to default (Customer)
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.user_role is None:
            if self.email == app.config['KATIES_ADMIN']:
                self.user_role = Role.query.filter_by(name='Administrator').first().id
        if self.user_role is None:
            self.user_role = Role.query.filter_by(default=True).first().id

    # Define permissions
    def can(self, permission):
        return (self.user_role is not None and self.user_role.has_permission(permission))

    def is_administrator(self):
        return self.can(Permission.ADMIN)
# endregion

# region AnonymousUser


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser

# endregion

# region Flavors


class IceCreamFlavors(db.Model):
    __tablename__ = 'IceCreamFlavors'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.Unicode, nullable=False)
    isRegularFlavor = db.Column(db.Boolean, nullable=False)
    isSherbet = db.Column(db.Boolean, nullable=False)
    hasSugar = db.Column(db.Boolean, nullable=False)

    @staticmethod
    def insert_flavors():
        flavors = (
            IceCreamFlavors(flavor="Banana", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Black Cherry",
                            isRegularFlavor=True, isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Cotton Candy",
                            isRegularFlavor=True, isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Bubble Gum", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Chocolate", isRegularFlavor=True,
                            isSherbet=False, hasSugar=True),
            IceCreamFlavors(flavor="Blue Boy", isRegularFlavor=False,
                            isSherbet=True, hasSugar=True),
            IceCreamFlavors(flavor="Orange", isRegularFlavor=False,
                            isSherbet=True, hasSugar=True),
            IceCreamFlavors(flavor="Red Raspberry",
                            isRegularFlavor=False, isSherbet=True, hasSugar=True),
            IceCreamFlavors(
                flavor="Cutter Pecan", isRegularFlavor=False, isSherbet=False, hasSugar=False),
            IceCreamFlavors(
                flavor="Fudge Ripple", isRegularFlavor=False, isSherbet=False, hasSugar=False),
            IceCreamFlavors(flavor="Vanilla", isRegularFlavor=False,
                            isSherbet=False, hasSugar=False)
        )
        for f in flavors:
            db.session.add(f)
        db.session.commit()
# endregion

# endregion

# region ForDebug

db.drop_all()
db.create_all()  # this is only needed if the database doesn't already exist

Role.insert_roles()
IceCreamFlavors.insert_flavors()

# endregion

# region Route Handlers

################
# Route Handlers
################

# region Home Page

###########
# Home Page
###########
@app.route("/")
def index():
    return render_template('home.j2', user=current_user)

# endregion

# region Login

#######
# Login
#######


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.j2', form=form, user=current_user)

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

# endregion

# region Register Customer

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
                user = User(email=form.email.data,
                            password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:  # if user already exists
                # flash warning message and redirect
                flash('There is already an account with that email address')
                return redirect(url_for('register'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('register'))

# endregion

# region Register Employee

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
                user = User(email=form.email.data,
                            password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:  # if user already exists
                # flash warning message and redirect
                flash('There is already an account with that email address')
                return redirect(url_for('register_employee'))
        else:
            for field, error in form.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for('register_employee'))

# endregion

# region Logout

########
# Logout
########
@app.get('/logout/')
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

# endregion

# region Flavors

#########
# Flavors
#########
@app.get('/flavors/')
def flavors():
    return render_template('flavors.j2', user=current_user, flavorList=IceCreamFlavors.query.all())

# endregion

# region Admin

##################
# Admin Management
##################
@app.route('/manage/')
@fresh_login_required
def manage():
    return render_template("manage.j2", user=current_user)

# endregion

# endregion
